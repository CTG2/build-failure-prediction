import json
from pathlib import Path

prediction = json.loads(
    Path("prediction.json").read_text(encoding="utf-8")
)

actual_result = Path("build_result.txt").read_text(
    encoding="utf-8"
).strip()

predicted_result = prediction["prediction"]

print("\n========== PREDICTION COMPARISON ==========")
print("Repository:", prediction["repository"])
print("Predicted result:", predicted_result)
print("Failure probability: {:.2%}".format(
    prediction["failure_probability"]
))
print("Actual Maven result:", actual_result)

if predicted_result == actual_result:
    print("Comparison: MATCH")
else:
    print("Comparison: MISMATCH")

print("===========================================")
