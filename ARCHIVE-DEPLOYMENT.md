# Archive legacy NeMo Retriever docs (docs-site branch)

Prepared branch: `docs/archive-banner-legacy-versions` (from `upstream/docs-site`).

## What changed

Injected an MkDocs Material **announcement banner** into all HTML pages for these **7 legacy versions**:

| Version | HTML pages updated |
|---|---|
| 25.3.0 | 468 |
| 25.4.2 | 468 |
| 25.6.2 | 468 |
| 25.6.3 | 472 |
| 25.9.0 | 479 |
| 26.1.1 | 290 |
| 26.1.2 | 318 |
| **Total** | **2,963** |

**Not archived (stay on live docs.nvidia.com):** `26.3.0`, `26.5.0`, `latest`.

184 pages were skipped because they already contained a Material `announce` component (search partials / non-content shells).

## Why not `repo.toml`?

The `docs-site` branch is a **pre-built MkDocs Material 9.6.7 static site** (mike versioned deploys). There is no Fern `repo.toml` in this branch. The equivalent of the TensorRT archive `announcement` setting is Material's `.md-banner` markup, injected after `<body>`.

Banner text:

> 📦 **Archived Documentation – Reference Only** — … For supported and up-to-date documentation, visit [NVIDIA Docs Hub: NeMo Retriever](https://docs.nvidia.com/nemo/retriever/latest/).

## S3 upload (manual — AWS console)

1. Go to https://awscloud.nvidia.com/ → **AWS Login** → **S3**.
2. Open bucket **`techdocs-assets-archive-prod`** (page 2).
3. Create folder structure matching live docs:

   ```
   nemo/retriever/25.3.0/
   nemo/retriever/25.4.2/
   nemo/retriever/25.6.2/
   nemo/retriever/25.6.3/
   nemo/retriever/25.9.0/
   nemo/retriever/26.1.1/
   nemo/retriever/26.1.2/
   ```

4. Upload the **contents** of each version folder from this branch (not the version folder name itself — mirror what's under `docs.nvidia.com/nemo/retriever/{version}/`).

   Local paths (after checkout):

   ```
   .worktrees/docs-site-archive-banner/25.3.0/*  →  s3://techdocs-assets-archive-prod/nemo/retriever/25.3.0/
   … (repeat for each version)
   ```

5. **Spot-check** one page on the archive host after upload, e.g.  
   `https://archive.docs.nvidia.com/nemo/retriever/25.3.0/extraction/overview/` — confirm the yellow banner appears at the top.

## Jira redirect request (assign to Kiran Kumar Gude)

Paste into your existing P0 ticket:

```
Please create redirects for archived NeMo Retriever documentation:

From: https://docs.nvidia.com/nemo/retriever/25.3.0/*
To:   https://archive.docs.nvidia.com/nemo/retriever/25.3.0/*

From: https://docs.nvidia.com/nemo/retriever/25.4.2/*
To:   https://archive.docs.nvidia.com/nemo/retriever/25.4.2/*

From: https://docs.nvidia.com/nemo/retriever/25.6.2/*
To:   https://archive.docs.nvidia.com/nemo/retriever/25.6.2/*

From: https://docs.nvidia.com/nemo/retriever/25.6.3/*
To:   https://archive.docs.nvidia.com/nemo/retriever/25.6.3/*

From: https://docs.nvidia.com/nemo/retriever/25.9.0/*
To:   https://archive.docs.nvidia.com/nemo/retriever/25.9.0/*

From: https://docs.nvidia.com/nemo/retriever/26.1.1/*
To:   https://archive.docs.nvidia.com/nemo/retriever/26.1.1/*

From: https://docs.nvidia.com/nemo/retriever/26.1.2/*
To:   https://archive.docs.nvidia.com/nemo/retriever/26.1.2/*
```

Assign to **Kiran Kumar Gude** for redirect implementation.

## After redirects are live

1. Verify each From URL 301/302 → archive URL.
2. Delete the **original** version folders from the live docs S3 bucket (per archive prerequisites — only after redirect is confirmed).
3. Restore per-version release-note links in `docs/docs/extraction/releasenotes.md` on `main` (currently blocked on #2326 / archive infra).

## Re-run banner injection

```powershell
python inject_archive_banner.py
```

Idempotent — pages that already have the banner are skipped.
