document.getElementById("generateBtn").addEventListener("click", async () => {
  const goal = document.getElementById("goalInput").value.trim();
  const resultDiv = document.getElementById("result");
  const planOutput = document.getElementById("planOutput");
  const loading = document.getElementById("loading");

  if (!goal) {
    alert("Please enter a goal before generating.");
    return;
  }

  resultDiv.classList.add("hidden");
  loading.classList.remove("hidden");
  planOutput.textContent = "";

  try {
    const response = await fetch("/generate-plan", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ goal }),
    });

    const data = await response.json();
    loading.classList.add("hidden");
    resultDiv.classList.remove("hidden");

    if (data.error) {
      planOutput.textContent = `Error: ${data.error}`;
      return;
    }

    const tasks = data.plan;
   // const tf = data.timeframe_text || `${data.total_days} days`

    let outputText = `Goal: ${data.goal}\nTimeline: ${tf}\n\n`;

    tasks.forEach((t, i) => {
      outputText += `${i + 1}. ${t.task || "Untitled Task"}\n`;
      outputText += `   Max Duration: ${t.duration || "—"}\n`;
      outputText += `   Depends on: ${t.depends_on || "—"}\n`;
      if (t.description) outputText += `   Description: ${t.description}\n`;
      outputText += `\n`;
    });

    planOutput.textContent = outputText;
  } catch (err) {
    loading.classList.add("hidden");
    resultDiv.classList.remove("hidden");
    planOutput.textContent = `Error connecting to backend: ${err}`;
  }
});




