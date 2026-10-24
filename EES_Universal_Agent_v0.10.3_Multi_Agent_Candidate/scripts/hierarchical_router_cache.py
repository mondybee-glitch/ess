"""Fail-closed hierarchical route cache; cache entries are untrusted input."""
import argparse
import hashlib
import json
import os
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROUTES = ROOT / 'hierarchical-routing.json'
CACHE = ROOT / 'state' / 'route-cache.json'
FORBIDDEN = {'evidence', 'signed_evidence', 'release_decision', 'private_key', 'secret', 'credential'}

def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')

def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()

def load_routes():
    data = json.loads(ROUTES.read_text(encoding='utf-8'))
    if not isinstance(data.get('stage1_routes'), list) or not data['stage1_routes']:
        raise ValueError('routing policy missing stage1_routes; refusing fallback')
    seen = set()
    for route in data['stage1_routes']:
        if not isinstance(route, dict) or not isinstance(route.get('id'), str) or not route['id'] or route['id'] in seen:
            raise ValueError('invalid or duplicate route id')
        if not isinstance(route.get('name'), str) or not isinstance(route.get('skills', []), list):
            raise ValueError('invalid route schema')
        seen.add(route['id'])
    return data

def cache_key(task, route_doc, model, policy_version):
    return digest({'task': task, 'routing_sha256': hashlib.sha256(ROUTES.read_bytes()).hexdigest(), 'model': model, 'policy_version': policy_version})

def validate_cached_route(route, route_doc):
    if not isinstance(route, dict):
        return False
    allowed = {r['id']: r for r in route_doc['stage1_routes']}
    route_id = route.get('id')
    # Cached data must match the current authoritative route definition exactly.
    return isinstance(route_id, str) and route_id in allowed and route == allowed[route_id]

def atomic_write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=path.name + '.', suffix='.tmp', dir=str(path.parent))
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(content); f.flush(); os.fsync(f.fileno())
        os.replace(tmp_name, path)
    finally:
        try: os.unlink(tmp_name)
        except FileNotFoundError: pass

def select(task, model='gemini', policy_version='1', ttl=900):
    if not isinstance(task, str) or len(task) > 100_000:
        raise ValueError('task must be a string no longer than 100000 characters')
    if not isinstance(model, str) or not model or len(model) > 128:
        raise ValueError('invalid model identifier')
    if not isinstance(policy_version, str) or not policy_version or len(policy_version) > 64:
        raise ValueError('invalid policy version')
    routes = load_routes(); key = cache_key(task, routes, model, policy_version); now = int(time.time())
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    db = {'schema_version': 1, 'entries': {}}
    if CACHE.exists():
        try:
            loaded = json.loads(CACHE.read_text(encoding='utf-8'))
            if isinstance(loaded, dict) and loaded.get('schema_version') == 1 and isinstance(loaded.get('entries'), dict):
                db = loaded
        except (OSError, ValueError, TypeError):
            # Corrupt cache is disposable. Never trust or execute its contents.
            db = {'schema_version': 1, 'entries': {}}
    ent = db['entries'].get(key)
    if isinstance(ent, dict) and ent.get('expires_at', 0) > now and validate_cached_route(ent.get('route'), routes):
        return {'cache': 'HIT', 'cache_key': key, 'route': ent['route'], 'expires_at': ent['expires_at'], 'provider_cache': 'NOT_CONFIGURED'}
    text = task.lower(); scores = []
    for route in routes['stage1_routes']:
        words = set(route['name'].lower().replace('&', ' ').split())
        skill_words = set(' '.join(route.get('skills', [])).replace('-', ' ').lower().split())
        score = sum(1 for word in words | skill_words if len(word) > 2 and word in text)
        scores.append((score, route))
    scores.sort(key=lambda pair: (pair[0], pair[1]['id']), reverse=True)
    chosen = scores[0][1] if scores and scores[0][0] > 0 else {'id': 'route-fallback', 'name': 'General engineering triage', 'skills': []}
    expires = now + max(1, min(int(ttl), 86400))
    db['entries'][key] = {'route': chosen, 'created_at': now, 'expires_at': expires, 'model': model, 'policy_version': policy_version}
    db['entries'] = {k: v for k, v in db['entries'].items() if isinstance(v, dict) and v.get('expires_at', 0) > now and validate_cached_route(v.get('route'), routes)}
    if len(db['entries']) > 500:
        db['entries'] = dict(list(db['entries'].items())[-500:])
    atomic_write(CACHE, json.dumps(db, indent=2, ensure_ascii=False) + '\n')
    return {'cache': 'MISS', 'cache_key': key, 'route': chosen, 'expires_at': expires, 'provider_cache': 'NOT_CONFIGURED'}

def invalidate():
    if CACHE.exists(): CACHE.unlink(); return True
    return False

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('action', choices=['select', 'invalidate']); ap.add_argument('--task', default=''); ap.add_argument('--model', default='gemini'); ap.add_argument('--policy-version', default='1'); ap.add_argument('--ttl', type=int, default=900); args = ap.parse_args()
    if args.action == 'invalidate': print(json.dumps({'invalidated': invalidate()})); return 0
    print(json.dumps(select(args.task, args.model, args.policy_version, args.ttl), indent=2, ensure_ascii=False)); return 0
if __name__ == '__main__': raise SystemExit(main())
