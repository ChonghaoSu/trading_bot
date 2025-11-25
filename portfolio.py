"""
Portfolio Holdings - Your Current Positions
Update this file whenever you buy/sell stocks
"""

# =============================================================================
# YOUR CURRENT HOLDINGS (as of November 2025)
# =============================================================================
# Each holding includes:
# - symbol: Stock ticker
# - shares: Number of shares owned (can be fractional)
# - avg_cost: Average cost per share in USD

holdings = [
    {"symbol": "GOOG", "shares": 0.679, "avg_cost": 294.56},
    {"symbol": "SMH",  "shares": 0.898, "avg_cost": 333.98},
    {"symbol": "META", "shares": 0.17,  "avg_cost": 586.65},
    {"symbol": "VPU",  "shares": 2.606, "avg_cost": 191.85},
    {"symbol": "TSLA", "shares": 0.248, "avg_cost": 403.79},
    {"symbol": "VGT",  "shares": 0.684, "avg_cost": 731.51},
    {"symbol": "RKLB", "shares": 1.222, "avg_cost": 40.90},
    {"symbol": "PLTR", "shares": 0.316, "avg_cost": 158.20},
    {"symbol": "NVDA", "shares": 1.121, "avg_cost": 183.27},
]


# =============================================================================
# STOCK WATCHLIST FOR RECOMMENDATIONS
# =============================================================================
# Add symbols here that you want the bot to analyze for buying opportunities
# The bot will check these against the momentum + pullback criteria

watchlist = [
    # =============================================================================
    # TECHNOLOGY - Major Tech & Cloud
    # =============================================================================
    # FAANG+ & Mega Cap Tech
    "AAPL", "MSFT", "AMZN", "GOOGL", "GOOG", "META", "NVDA", "TSLA",
    
    # Cloud & SaaS
    "CRM", "NOW", "WDAY", "TEAM", "ZM", "DOCN", "NET", "FTNT",
    "PANW", "ZS", "CRWD", "S", "OKTA", "ESTC", "DDOG", "SPLK",
    
    # Enterprise Software
    "ORCL", "ADBE", "INTU", "ADSK", "ANSS", "CDNS", "SNPS",
    
    # =============================================================================
    # TECHNOLOGY - Semiconductors & Hardware
    # =============================================================================
    # Chip Design & Manufacturing
    "AMD", "INTC", "AVGO", "TSM", "ASML", "MU", "QCOM", "NXPI",
    "MRVL", "SWKS", "QRVO", "MCHP", "ON", "WOLF", "MPWR",
    
    # Semiconductor Equipment
    "AMAT", "LRCX", "KLAC", "ENTG", "TER",
    
    # Hardware & Components
    "DELL", "HPQ", "HPE", "CSCO", "ANET", "ARISTA",
    
    # =============================================================================
    # TECHNOLOGY - AI & Machine Learning
    # =============================================================================
    "PLTR", "SNOW", "AI", "PATH", "AI", "C3AI", "BBAI",
    
    # =============================================================================
    # TECHNOLOGY - Fintech & Payments
    # =============================================================================
    "SQ", "PYPL", "COIN", "HOOD", "SOFI", "AFRM", "UPST", "LC",
    
    # =============================================================================
    # TECHNOLOGY - Gaming & Entertainment
    # =============================================================================
    "NFLX", "RBLX", "EA", "TTWO", "ATVI", "U", "DKNG",
    
    # =============================================================================
    # TECHNOLOGY - E-commerce & Retail Tech
    # =============================================================================
    "SHOP", "ETSY", "MELI", "SE", "MARA", "RIOT",
    
    # =============================================================================
    # TECHNOLOGY - Cybersecurity
    # =============================================================================
    "CRWD", "ZS", "PANW", "FTNT", "S", "QLYS", "TENB", "RPD",
    
    # =============================================================================
    # ENERGY - Oil & Gas
    # =============================================================================
    # Integrated Oil
    "XOM", "CVX", "COP", "SLB", "HAL", "OXY", "MPC", "VLO",
    
    # Exploration & Production
    "EOG", "DVN", "FANG", "MRO", "CTRA", "PR", "MTDR",
    
    # Midstream & Pipelines
    "ENB", "EPD", "KMI", "OKE", "WMB", "TRP",
    
    # =============================================================================
    # ENERGY - Renewable & Clean Energy
    # =============================================================================
    # Solar
    "ENPH", "SEDG", "FSLR", "RUN", "NOVA", "ARRY", "NEXT",
    
    # Wind
    "BEP", "BEPC", "NEE", "AES",
    
    # Battery & Storage
    "TSLA", "ENPH", "SEDG", "PLUG", "BE", "CHPT", "EVGO",
    
    # Hydrogen
    "PLUG", "BE", "FCEL", "BLDP",
    
    # =============================================================================
    # ENERGY - Utilities
    # =============================================================================
    "NEE", "DUK", "SO", "AEP", "D", "EXC", "SRE", "XEL",
    
    # =============================================================================
    # REAL ESTATE - Data Centers
    # =============================================================================
    # Data Center REITs
    "EQIX", "DLR", "CONE", "AMT", "CCI", "SBAC",
    
    # Data Center Infrastructure
    "ANET", "CSCO", "JNPR", "FFIV",
    
    # =============================================================================
    # REAL ESTATE - Infrastructure REITs
    # =============================================================================
    # Tower REITs (5G infrastructure)
    "AMT", "CCI", "SBAC",
    
    # =============================================================================
    # REAL ESTATE - General REITs
    # =============================================================================
    # Industrial & Logistics
    "PLD", "EXPI", "PSA",
    
    # Office
    "BXP", "VNO", "SLG",
    
    # Residential
    "EQR", "AVB", "MAA", "UDR",
    
    # Retail
    "SPG", "O", "MAC",
    
    # Healthcare REITs
    "WELL", "PEAK", "VTR",
    
    # =============================================================================
    # EDUCATION - Online Learning & EdTech
    # =============================================================================
    # Online Education Platforms
    "COUR", "LAUR", "LRN", "EDU", "TAL", "GSX",
    
    # Educational Technology
    "CHGG", "U", "TWOU", "STRA",
    
    # =============================================================================
    # EDUCATION - Traditional Education
    # =============================================================================
    # For-Profit Education
    "APEI", "LOPE", "GHC",
    
    # Educational Services
    "BFAM", "EDU", "TAL",
    
    # =============================================================================
    # INDEX ETFs - Broad Market
    # =============================================================================
    "SPY", "QQQ", "IWM", "DIA", "VOO", "VTI", "SPLG",
    
    # =============================================================================
    # SECTOR ETFs
    # =============================================================================
    # Technology
    "XLK", "VGT", "FTEC", "IGV", "SOXX", "SMH",
    
    # Energy
    "XLE", "VDE", "IYE", "FENY",
    
    # Real Estate
    "VNQ", "SCHH", "VNQI", "IYR",
    
    # =============================================================================
    # GROWTH & INNOVATION ETFs
    # =============================================================================
    "ARKK", "ARKQ", "ARKG", "ARKF", "ARKW",
    "QQQM", "QQQJ", "VUG", "MGK",
    
    # =============================================================================
    # SPACE & INNOVATION
    # =============================================================================
    "RKLB", "LUNR", "ASTS", "SPCE", "RDW",
    
    # =============================================================================
    # ELECTRIC VEHICLES
    # =============================================================================
    "TSLA", "RIVN", "LCID", "F", "GM", "FORD",
    
    # =============================================================================
    # BIOTECH & HEALTHCARE TECH
    # =============================================================================
    "MRNA", "BNTX", "GILD", "REGN", "VRTX", "BIIB",
]


def get_portfolio_value(current_prices: dict) -> dict:
    """
    Calculate total portfolio metrics
    
    Args:
        current_prices: Dictionary mapping symbols to current prices
        
    Returns:
        Dictionary with portfolio statistics
    """
    total_cost = 0
    total_value = 0
    position_details = []
    
    for holding in holdings:
        symbol = holding["symbol"]
        shares = holding["shares"]
        avg_cost = holding["avg_cost"]
        
        cost_basis = shares * avg_cost
        total_cost += cost_basis
        
        if symbol in current_prices:
            current_price = current_prices[symbol]
            current_value = shares * current_price
            total_value += current_value
            
            pnl = current_value - cost_basis
            pnl_percent = (pnl / cost_basis) * 100 if cost_basis > 0 else 0
            
            position_details.append({
                "symbol": symbol,
                "shares": shares,
                "avg_cost": avg_cost,
                "current_price": current_price,
                "cost_basis": cost_basis,
                "current_value": current_value,
                "pnl": pnl,
                "pnl_percent": pnl_percent
            })
    
    total_pnl = total_value - total_cost
    total_pnl_percent = (total_pnl / total_cost) * 100 if total_cost > 0 else 0
    
    return {
        "total_cost": total_cost,
        "total_value": total_value,
        "total_pnl": total_pnl,
        "total_pnl_percent": total_pnl_percent,
        "positions": position_details
    }


def format_currency(amount: float) -> str:
    """Format a number as USD currency"""
    return f"${amount:,.2f}"


def format_percent(percent: float) -> str:
    """Format a number as percentage with sign"""
    sign = "+" if percent >= 0 else ""
    return f"{sign}{percent:.2f}%"

