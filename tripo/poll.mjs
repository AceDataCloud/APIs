import { setTimeout as sleep } from "node:timers/promises";

async function poll(taskId, token) {
  const deadline = Date.now() + 10 * 60 * 1000;
  while (Date.now() < deadline) {
    const response = await fetch("https://api.acedata.cloud/tripo/tasks", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ id: taskId }),
      signal: AbortSignal.timeout(30000),
    });
    if (!response.ok) {
      throw new Error(`Task lookup returned HTTP ${response.status} for ${taskId}`);
    }

    const record = await response.json();
    if (!record.id) throw new Error(`Task ${taskId} was not found for this account`);
    if (typeof record.response?.success === "boolean") {
      console.log(JSON.stringify(record, null, 2));
      if (!record.response.success) process.exitCode = 1;
      return;
    }
    await sleep(5000);
  }
  throw new Error(`Still processing. Run the same command again with task ID ${taskId}.`);
}

const taskId = process.argv[2];
const token = process.env.ACEDATACLOUD_API_TOKEN;
if (!taskId || !token) {
  console.error("Set ACEDATACLOUD_API_TOKEN and run: node poll.mjs <task-id>");
  process.exitCode = 1;
} else {
  try {
    await poll(taskId, token);
  } catch (error) {
    console.error(error.message);
    process.exitCode = 1;
  }
}
