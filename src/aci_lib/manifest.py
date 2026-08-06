"""Human-readable descriptions for known data/processed/ dataset name patterns.

Matched against catalog dataset names (see catalog.py) in order; the first
regex that matches wins. Names with no match get an empty description --
data/processed/ has grown organically (see ARCHITECTURE.md §2), so this list
covers the well-understood parts, not every file.
"""
import re

_PATTERNS = [
    (r"^percentiles(_temperatura)?$",
     "Baseline (1961-1990) T90/T10 percentile thresholds, from calcular_percentil_temperatura.py."),
    (r"^viento_percentiles$",
     "Baseline (1961-1990) wind-power P90 threshold, from calcular_percentil_viento.py."),
    (r"^era5_(temperatura|lluvia|lluvias|sequia|wind)_percentil$",
     "Gridded baseline percentile field (NetCDF) underlying the corresponding percentiles*.csv."),
    (r"^anomalias_(\w+)/anomalies_(temperature|precipitation|drought|wind)_combined$",
     "Monthly per-region anomaly series (combined CSV) -- ACI-CO component input, see ARCHITECTURE.md Stage 3."),
    (r"^anomalias_(\w+)/anomalies_(temperature|wind)$",
     "Gridded monthly anomaly fields (one NetCDF per year-month) underlying the corresponding _combined.csv series."),
    (r"^aci_daily/(rain|tmp|wind)$",
     "Daily gridded input to run_aci_colombia.py's from-scratch ACI cross-check (ARCHITECTURE.md §3)."),
    (r"^daily_by_year_(rain|tmp|wind)/",
     "Daily gridded ERA5 field split by year, feeding produce_daily_anomalies.py (Stage 4)."),
    (r"^daily_anomalies/anomalias_diarias(_\w+)?$",
     "Daily anomaly export per region (xlsx), from produce_daily_anomalies.py / append_2025_2026.py."),
    (r"^oni_", "ENSO ONI index variant (raw/resampled/feature-engineered) -- see compare_enso_flags.py."),
    (r"^ersst5\.nino", "ERSSTv5 Nino-region SST reference series used to validate the ERA5-derived ONI index."),
    (r"^sst_|^anomalies_sst_oni$",
     "Sea-surface-temperature / ENSO index series feeding the ENSO-neutral decomposition (article1.tex §4), from anomalias_sst_daily.py."),
    (r"^ungrd_monthly$",
     "UNGRD national disaster registry, monthly event counts by type -- input to the §7 validation regression."),
    (r"^era5_ideam_comparison/",
     "ERA5 vs. IDEAM station bias comparison outputs, from bias_era5_ideam.py."),
    (r"^downscaled/",
     "High-resolution (0.01deg) downscaled ERA5 fields (RandomForest), Stage 6 of the pipeline."),
    (r"^threshold_search_results$",
     "Wind-power threshold sensitivity search (parametric mu+1.28sigma vs. empirical P90 -- see article1.tex §3.3)."),
    (r"^aci_colombia_partial$|^aci_python_output_1961_1990$",
     "run_aci_colombia.py cross-check output, diffed against the OPT pipeline by compare_aci_colombia.py / compare_repos.py."),
    (r"^colombia_era5_mask$", "Land/sea grid mask used to restrict ERA5 fields to Colombian territory."),
    (r"^enso_flag_comparison$", "Comparison of ENSO phase flags derived from different ONI sources."),
    (r"^nino3_reference$", "Reference Nino-3.4 index series used to sanity-check the ERA5-derived SST index."),
]

_COMPILED = [(re.compile(p), d) for p, d in _PATTERNS]


def describe(name):
    for pattern, description in _COMPILED:
        if pattern.search(name):
            return description
    return ""
