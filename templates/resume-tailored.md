<!--
Markdown layout for a tailored resume (stage 7), rendered from resume.json.
Keep it ATS-friendly: single column, plain text, no tables/columns/graphics/text-boxes.
Use standard section names. Omit any section that's empty. Delete this comment on output.
Every line must trace to a corpus entry — see references/07-tailoring.md.
-->

# {{ basics.name }}

{{ basics.label }} · {{ basics.email }}{{ " · " + basics.phone if phone }}{{ " · " + location if location }}
{{ profiles as "· LinkedIn: <url>" etc., if present }}

## Summary

{{ basics.summary — one to three lines, truthfully targeted at this role }}

## Experience

### {{ work.position }} — {{ work.name }}
{{ work.startDate }} – {{ work.endDate or "Present" }}{{ ", " + work.location if present }}

- {{ highlight — XYZ bullet: accomplished X, as measured by Y, by doing Z }}
- {{ ... strongest, most on-target bullets first; drop Y honestly if no real metric }}

<!-- repeat per work entry, most relevant/recent first -->

## Projects
<!-- include only if relevant to this posting -->

### {{ project.name }}
- {{ highlight }}

## Skills

{{ grouped, comma-separated; mirror the posting's terms only for skills genuinely held }}

## Education

{{ education.studyType }} in {{ education.area }} — {{ education.institution }}{{ ", " + endDate }}

## Certificates
<!-- include only if present -->

{{ certificate.name }} — {{ certificate.issuer }}{{ ", " + date }}

<!-- Optional, only if relevant to the role: Awards, Volunteer, Languages, Interests -->
