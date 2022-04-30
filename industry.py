def get_industry():
    """List og the different sectors"""
    industry_names = [
        {"name": "Energy"},
        {"name": "Materials"},
        {"name": "Industrials"},
        {"name": "Consumer Discretionary"},
        {"name": "Consumer Staples"},
        {"name": "Health Care"},
        {"name": "Financials"},
        {"name": "Information Technology"},
        {"name": "Telecommunication Services"},
        {"name": "Utilities"}
    ]

    for industry in industry_names:
        industry["procent"] = 0

    return industry_names


def get_sector_names():
    """List of the different industry groups"""
    sector_names = [
        {"name": "Process Industries"},
        {"name": "Consumer Durables"},
        {"name": "Manufacturing"},
        {"name": "Arts, Entertainment, and Recreation"},
        {"name": "Health Care and Social Assistance"},
        {"name": "Electronic Technology"},
        {"name": "Wholesale Trade"},
        {"name": "Communications"},
        {"name": "Transportation"},
        {"name": "Miscellaneous"},
        {"name": "Agriculture, Forestry, Fishing and Hunting"},
        {"name": "Educational Services"},
        {"name": "Professional, Scientific, and Technical Services"},
        {"name": "Management of Companies and Enterprises"},
        {"name": "Health Technology"},
        {"name": "Finance and Insurance"},
        {"name": "Retail Trade"},
        {"name": "Public Administration"},
        {"name": "Commercial Services"},
        {"name": "Utilities"},
        {"name": "Distribution Services"},
        {"name": "Non-Energy Minerals"},
        {"name": "Administrative and Support and Waste Management and Remediation Services"},
        {"name": "Accommodation and Food Services"},
        {"name": "Mining, Quarrying, and Oil and Gas Extraction"},
        {"name": "Real Estate and Rental and Leasing"},
        {"name": "Producer Manufacturing"},
        {"name": "Energy Minerals"},
        {"name": "Information"},
        {"name": "Consumer Non-Durables"},
        {"name": "Transportation and Warehousing"},
        {"name": "Other Services (except Public Administration)"},
        {"name": "Finance"},
        {"name": "Health Services"},
        {"name": "Government"},
        {"name": "Construction"},
        {"name": "Industrial Services"},
        {"name": "Technology Services"},
        {"name": "Consumer Services"}
    ]

    for sector in sector_names:
        sector["procent"] = 0

    return sector_names
