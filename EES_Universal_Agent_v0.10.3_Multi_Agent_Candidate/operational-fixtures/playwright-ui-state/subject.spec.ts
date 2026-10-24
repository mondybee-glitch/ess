import { test, expect } from '@playwright/test';
import { createServer } from 'node:http';
import type { AddressInfo } from 'node:net';
let server: ReturnType<typeof createServer>; let url = '';
test.beforeAll(async () => {
 server = createServer((_req, res) => { res.writeHead(200, {'content-type':'text/html; charset=utf-8'}); res.end('<!doctype html><html><body><button id="save">Save</button><p role="status" aria-live="polite"></p><script>document.querySelector("#save").addEventListener("click",()=>document.querySelector("[role=status]").textContent="Saved")</script></body></html>'); });
 await new Promise<void>(resolve => server.listen(0, '127.0.0.1', resolve));
 url = `http://127.0.0.1:${(server.address() as AddressInfo).port}`;
});
test.afterAll(async () => { await new Promise<void>((resolve,reject) => server.close(err => err ? reject(err) : resolve())); });
test('keyboard activation updates accessible status', async ({ page }) => {
 await page.goto(url); await page.getByRole('button', {name:'Save'}).focus(); await page.keyboard.press('Enter');
 await expect(page.getByRole('status')).toHaveText('Saved');
});

test('renders a visible keyboard focus indicator and supports narrow viewport', async ({ page }) => {
 await page.setViewportSize({ width: 320, height: 720 });
 await page.goto(url);
 const button = page.getByRole('button', {name:'Save'});
 await button.focus();
 await expect(button).toBeFocused();
 const box = await button.boundingBox();
 expect(box).not.toBeNull();
 expect(box!.x).toBeGreaterThanOrEqual(0);
 expect(box!.x + box!.width).toBeLessThanOrEqual(321);
});
test('status remains exposed to assistive technology', async ({ page }) => {
 await page.goto(url);
 await expect(page.getByRole('status')).toHaveAttribute('aria-live', 'polite');
});
