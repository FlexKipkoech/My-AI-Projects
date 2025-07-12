# Fix Kenya Document Generator Configuration

# Document types mapping
DOCUMENT_TYPES = {
    "Market Research Only": "market_research",
    "Strategy Document Only": "strategy", 
    "Both Documents": "both"
}

# Priority levels
PRIORITY_LEVELS = ["normal", "high", "urgent"]

# Estimated generation times (in minutes)
GENERATION_TIMES = {
    "market_research": 5,
    "strategy": 5,
    "both": 10
}

# Company information
COMPANY_INFO = {
    "name": "Fix Kenya Limited",
    "email": "info@fix.co.ke",
    "phone": "+254 723 278 375",
    "website": "www.fix.co.ke",
    "support_email": "support@fix.co.ke"
}

# Form validation rules
VALIDATION_RULES = {
    "min_business_description": 50,  # minimum characters
    "min_objectives": 2,  # minimum number of objectives
    "max_competitors": 10  # maximum number of competitors
}

# Industries list (for dropdown)
INDUSTRIES = [
    "Technology",
    "Retail",
    "Healthcare", 
    "Financial Services",
    "Manufacturing",
    "Education",
    "Real Estate",
    "Tourism & Hospitality",
    "Agriculture",
    "Transportation & Logistics",
    "Energy & Utilities",
    "Media & Entertainment",
    "Non-Profit",
    "Other"
]

# Common objectives (for suggestions)
COMMON_OBJECTIVES = [
    "Increase brand awareness",
    "Generate qualified leads",
    "Improve customer engagement",
    "Increase online sales",
    "Build thought leadership",
    "Expand market reach",
    "Improve customer retention",
    "Launch new product/service",
    "Enter new market segment",
    "Optimize digital presence"
]