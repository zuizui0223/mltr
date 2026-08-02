# Paper A format audit against Theoretical Ecology submission guidelines

Audit date: 2026-07-23

Official source checked: Theoretical Ecology, Springer Nature, Submission guidelines.

## Confirmed compliant

- Manuscript is supplied as editable LaTeX and builds to PDF.
- Abstract length is 197 words, within the required 150--250 words.
- Six keywords are supplied, within the required 4--6 keywords.
- In-text citations use author--year form.
- References are alphabetized by first author in the compiled bibliography.
- Tables and figures are numbered and cited consecutively.
- Figures are embedded in the body of the manuscript.
- Supplementary text is supplied as PDF-compatible LaTeX output.
- Main manuscript, supplement, CI, and reproducibility workflows pass on commit 5cb2a470720334c4c9446003d2cbcc1770f2c6fd.

## Corrected in this PR

- Added `hidelinks` to the supplementary manuscript so internal hyperlinks do not appear as red boxes in the delivered PDF.
- Identified the supplement as `Online Resource 1` and named the target journal in the supplement title.
- Reworked Figure 1 into a legible two-column, three-row ecological workflow.
- Replaced the over-dense four-column literature table with a readable three-column table.
- Added verified author--year citations and bibliography integration.

## Objective format gaps still requiring repository changes

1. **Main-PDF hyperlink appearance**
   - The compiled main PDF currently displays colored citation links and red link boxes.
   - Add `\hypersetup{hidelinks}` to `paper_a_main.tex`.

2. **Titles inside figures**
   - Springer instructs authors not to include titles or captions inside illustrations.
   - The three generated SVG figures currently contain internal title lines.
   - Remove those title lines; retain the explanatory text only in the manuscript captions.

3. **Figure captions**
   - The journal requests captions beginning with `Fig.` in bold and no terminal punctuation.
   - The generic `article` class currently produces `Figure 1:` and captions ending in periods.
   - Prefer the Springer Nature LaTeX template, or configure the caption package explicitly.

4. **Springer Nature LaTeX template**
   - Mathematical manuscripts may be submitted in LaTeX, and the journal recommends the Springer Nature template.
   - The current manuscript uses the generic `article` class. This is editable and compilable, but it is not template-conformant.
   - Before final submission, migrate to the current Springer Nature `sn-jnl` template and rerun all PDF checks.

5. **Statements and Declarations**
   - The journal requires a `Statements and Declarations` section after the References.
   - It must include Funding and Competing Interests; Author Contributions are encouraged.
   - These statements are absent from the current manuscript.

6. **Data Availability Statement**
   - Original research articles must contain a Data Availability Statement.
   - For this theoretical paper, the statement should clarify that no empirical data were generated and identify the repository/archived release containing code and finite verification cases.

7. **Supplementary identification details**
   - Each supplementary file must contain the article title, journal name, author names, affiliation, and corresponding-author email.
   - Journal and article identification are now present.
   - Author, affiliation, and email remain unresolved until the final author list is supplied.

## Author-supplied submission blockers

The following cannot be inferred safely from the repository and must be supplied by the authors before the manuscript is marked submission-ready:

- complete author names and order;
- author affiliations;
- corresponding author and active email;
- ORCID identifiers, if available;
- acknowledgments;
- funding statement and grant numbers, or an explicit no-funding statement;
- competing-interest statement;
- author-contribution statement;
- final public archive/DOI for code and verification materials;
- five suggested reviewers for the cover letter.

## Current verdict

The manuscript is scientifically buildable and visually improved, but it is **not yet formally submission-ready** for Theoretical Ecology. The outstanding work is concentrated in Springer-template migration, declarations/data availability, figure-caption conventions, removal of internal figure titles, and final author metadata.
