"""Validate shared issue forms without creating GitHub issues."""
from pathlib import Path
import yaml

root = Path(__file__).resolve().parents[1]
templates = root / ".github" / "ISSUE_TEMPLATE"
form = yaml.safe_load((templates / "bug_report.yml").read_text())
assert form["type"] == "Bug"
fields = {item["attributes"]["label"]: item for item in form["body"] if "id" in item}
assert list(fields) == [
    "Report format", "Product", "Interested customers", "Version", "Environment",
    "Actual result", "Expected result", "Steps to reproduce", "Impact", "Severity", "Evidence",
]
assert len({item["id"] for item in fields.values()}) == len(fields)
assert fields["Report format"]["attributes"]["options"] == ["ROCC bug report v1"]
assert fields["Report format"]["attributes"]["default"] == 0
assert fields["Report format"]["type"] == "dropdown"  # Markdown blocks are not submitted.
assert fields["Product"]["attributes"]["multiple"] is True
assert fields["Interested customers"]["type"] == "input"  # Never publish a private customer roster.
assert "value" not in fields["Interested customers"]["attributes"]
assert fields["Version"]["validations"]["required"] is True
for label, item in fields.items():
    assert item["type"] in {"input", "textarea", "dropdown"}
    assert item["validations"]["required"] is (label != "Evidence")
    if item["type"] == "dropdown":
        options = item["attributes"]["options"]
        assert len(options) == len(set(options))
        if "default" in item["attributes"]:
            assert 0 <= item["attributes"]["default"] < len(options)
assert yaml.safe_load((templates / "config.yml").read_text())["blank_issues_enabled"] is True
assert not (templates / "bug_report.md").exists()
assert not (templates / "backport-request.md").exists()
for filename, issue_type in [("feature_request.md", "Feature"), ("task.md", "Task")]:
    frontmatter = (templates / filename).read_text().split("---", 2)[1]
    assert yaml.safe_load(frontmatter)["type"] == issue_type
for filename in ["decision.md", "risk.md"]:
    assert (templates / filename).is_file()

# Model the body GitHub creates from submitted answers. In particular, a visible
# dropdown persists the format marker while introductory markdown does not.
answers = {label: "Example" for label in fields}
answers["Report format"] = "ROCC bug report v1"
answers["Product"] = "Core, Resolve"
answers["Version"] = "12.11.2"
body = "\n\n".join(f"### {label}\n\n{answers[label]}" for label in fields)
assert "### Report format\n\nROCC bug report v1" in body
assert "### Version\n\n12.11.2" in body
print("PASS: shared form schema, submitted-body contract, privacy and retained templates")
