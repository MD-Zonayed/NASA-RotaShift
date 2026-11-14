# RotaShift — Speaker Notes for the Seven-Slide Demo

## Slide 1 — Title
Introduce Soil-to-Sky Robo Team, the Dhaka Local Event, the Field Shift challenge, and RotaShift. Add all five other registered team-member names on the slide before publishing. State that the Farmbot shown is existing research.

## Slide 2 — Problem
Explain that rotation choice is multi-factor: temperature, rainfall, water, soil condition, and farmer priorities. The current catalogue contains 13 crops across three seasonal slots, giving 72 combinations under the current one-crop-per-slot rule.

## Slide 3 — Workflow
Walk through site selection, climate/soil/irrigation assumptions, farmer priority weights, and ranked rotation outputs. Be precise: NASA POWER climate inputs feed the score; SMAP and MODIS are currently context visualisations only.

## Slide 4 — NASA data
Show actual processed MODIS NDVI values from the included exports: 14/22 composites for Uttara, 16/22 for Araihazar. Explain that SMAP quality is weak near the reference points: no flag-0 observations within 9 km, and the Uttara flag-0 pixels are about 15.12 km away in the wider export. SMAP is regional context, not field validation.

## Slide 5 — Farmbot
Show the real field prototype and supplied YOLOv8 ripe/unripe tomato detection image. Mention the linked YouTube video as prior Farmbot work, not as the required RotaShift demo. Do not claim disease diagnosis.

## Slide 6 — Decision engine
Explain the rule-based dimensions and data sources. BARC nutrient rows are reference ranges, not automatic prescriptions. The rice variety/yield groups are incomplete; nine crop-water references come from BRRI modelled studies and four are FAO-56 planning estimates. Drought tolerance/income values are relative scores.

## Slide 7 — Impact and limitations
Describe the prototype's intended value, then proactively disclose no real sensor export/calibration, no HLS outputs, approximate coordinates, SMAP quality limitations, and no yield validation. State that the next step is field GPS, lab soil tests, real sensor records, and farmer review.

## Presenter checklist
- Replace the five teammate-name placeholders.
- Keep the deck at exactly seven slides.
- Upload the PPTX to a public Drive/OneDrive/GitHub link and test in an incognito window.
- Use the public GitHub repository as the final-project link.
- Keep the Farmbot video as supplementary prior-work media.
- Do not use synthetic demo data as measured evidence.
