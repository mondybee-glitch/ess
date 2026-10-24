#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sqlite3, time
from pathlib import Path

def connect(path: str):
    db=sqlite3.connect(path); db.execute('''CREATE TABLE IF NOT EXISTS feedback (id INTEGER PRIMARY KEY, task_id TEXT, skill_id TEXT, category TEXT, outcome TEXT, details TEXT, created_at REAL)'''); db.execute('''CREATE TABLE IF NOT EXISTS candidates (id INTEGER PRIMARY KEY, skill_id TEXT, reason TEXT, expected_benefit TEXT, regression_risk TEXT, status TEXT, created_at REAL)'''); db.commit(); return db

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--db',default='data/agent-memory.sqlite'); sub=ap.add_subparsers(dest='cmd',required=True)
    f=sub.add_parser('feedback'); f.add_argument('--task-id',required=True); f.add_argument('--skill-id',required=True); f.add_argument('--category',required=True); f.add_argument('--outcome',required=True); f.add_argument('--details',required=True)
    c=sub.add_parser('candidate'); c.add_argument('--skill-id',required=True); c.add_argument('--reason',required=True); c.add_argument('--expected-benefit',required=True); c.add_argument('--regression-risk',required=True)
    l=sub.add_parser('list'); l.add_argument('--skill-id')
    a=ap.parse_args(); Path(a.db).parent.mkdir(parents=True,exist_ok=True); db=connect(a.db)
    if a.cmd=='feedback': db.execute('INSERT INTO feedback(task_id,skill_id,category,outcome,details,created_at) VALUES(?,?,?,?,?,?)',(a.task_id,a.skill_id,a.category,a.outcome,a.details,time.time())); db.commit(); print(json.dumps({'status':'recorded','kind':'feedback'}))
    elif a.cmd=='candidate': db.execute('INSERT INTO candidates(skill_id,reason,expected_benefit,regression_risk,status,created_at) VALUES(?,?,?,?,?,?)',(a.skill_id,a.reason,a.expected_benefit,a.regression_risk,'candidate',time.time())); db.commit(); print(json.dumps({'status':'candidate_created'}))
    else:
        rows=db.execute('SELECT id,task_id,skill_id,category,outcome,details,created_at FROM feedback WHERE (? IS NULL OR skill_id=?) ORDER BY id DESC LIMIT 50',(a.skill_id,a.skill_id)).fetchall(); print(json.dumps([dict(zip(['id','task_id','skill_id','category','outcome','details','created_at'],r)) for r in rows],ensure_ascii=False))
    db.close()
if __name__=='__main__': main()
