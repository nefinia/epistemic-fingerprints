import assert from "node:assert/strict";
import test from "node:test";

async function render() {
  const workerUrl = new URL("../dist/server/index.js", import.meta.url);
  workerUrl.searchParams.set("test", `${process.pid}-${Date.now()}`);
  const { default: worker } = await import(workerUrl.href);
  return worker.fetch(
    new Request("http://localhost/", { headers: { accept: "text/html" } }),
    { ASSETS: { fetch: async () => new Response("Not found", { status: 404 }) } },
    { waitUntil() {}, passThroughOnException() {} },
  );
}

test("server-renders the Epistemic Fingerprints research app", async () => {
  const response = await render();
  assert.equal(response.status, 200);
  assert.match(response.headers.get("content-type") ?? "", /^text\/html\b/i);
  const html = await response.text();
  assert.match(html, /Epistemic Fingerprints/);
  assert.match(html, /Many agents/);
  assert.match(html, /Results observatory/);
  assert.match(html, /Pilot lab/);
  assert.match(html, /Simulated demo/);
  assert.match(html, /More output is not necessarily more exploration/);
  assert.match(html, /Agreement can be a correlated failure/);
  assert.match(html, /SAFETY PROBE/);
  assert.match(html, /MARGINAL EPISTEMIC GAIN/);
  assert.match(html, /How to read Figure 1/);
  assert.match(html, /Shumailov et al/);
  assert.doesNotMatch(html, /codex-preview|Your site is taking shape|react-loading-skeleton/i);
});
