// Trading Bot UI JavaScript

// Toast notification
function showToast(message, isError = false) {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = 'toast' + (isError ? ' error' : '');
    toast.classList.add('show');
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Holdings Management
async function addHolding(event) {
    event.preventDefault();
    
    const symbol = document.getElementById('holding-symbol').value.toUpperCase();
    const shares = parseFloat(document.getElementById('holding-shares').value);
    const avgCost = parseFloat(document.getElementById('holding-cost').value);
    
    try {
        const response = await fetch('/api/holdings', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ symbol, shares, avg_cost: avgCost })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showToast('✅ Holding added successfully!');
            event.target.reset();
            loadHoldings();
        } else {
            showToast('❌ ' + (data.error || 'Failed to add holding'), true);
        }
    } catch (error) {
        showToast('❌ Error: ' + error.message, true);
    }
}

async function deleteHolding(symbol) {
    if (!confirm(`Delete ${symbol} from holdings?`)) {
        return;
    }
    
    try {
        const response = await fetch(`/api/holdings/${symbol}`, {
            method: 'DELETE'
        });
        
        const data = await response.json();
        
        if (data.success) {
            showToast('✅ Holding deleted successfully!');
            loadHoldings();
        } else {
            showToast('❌ Failed to delete holding', true);
        }
    } catch (error) {
        showToast('❌ Error: ' + error.message, true);
    }
}

async function loadHoldings() {
    try {
        const response = await fetch('/api/holdings');
        const holdings = await response.json();
        
        const tbody = document.getElementById('holdings-body');
        let totalCostBasis = 0;
        let totalCurrentValue = 0;
        
        tbody.innerHTML = holdings.map(h => {
            const costBasis = h.shares * h.avg_cost;
            totalCostBasis += costBasis;
            
            if (h.current_price !== null && h.current_price !== undefined) {
                const currentValue = h.current_value || (h.shares * h.current_price);
                totalCurrentValue += currentValue;
                
                const pnl = h.pnl || (currentValue - costBasis);
                const pnlPercent = h.pnl_percent || ((h.current_price - h.avg_cost) / h.avg_cost * 100);
                
                const pnlClass = pnl >= 0 ? 'positive' : 'negative';
                const pnlSign = pnl >= 0 ? '+' : '';
                
                return `
                    <tr data-symbol="${h.symbol}">
                        <td><strong>${h.symbol}</strong></td>
                        <td>${parseFloat(h.shares).toFixed(3)}</td>
                        <td>$${parseFloat(h.avg_cost).toFixed(2)}</td>
                        <td class="current-price">$${parseFloat(h.current_price).toFixed(2)}</td>
                        <td class="current-value">$${currentValue.toFixed(2)}</td>
                        <td class="pnl ${pnlClass}">${pnlSign}$${Math.abs(pnl).toFixed(2)}</td>
                        <td class="pnl-percent ${pnlClass}">${pnlSign}${Math.abs(pnlPercent).toFixed(2)}%</td>
                        <td>
                            <button class="btn-danger btn-sm" onclick="deleteHolding('${h.symbol}')">Delete</button>
                        </td>
                    </tr>
                `;
            } else {
                return `
                    <tr data-symbol="${h.symbol}">
                        <td><strong>${h.symbol}</strong></td>
                        <td>${parseFloat(h.shares).toFixed(3)}</td>
                        <td>$${parseFloat(h.avg_cost).toFixed(2)}</td>
                        <td class="current-price">N/A</td>
                        <td class="current-value">-</td>
                        <td class="pnl">-</td>
                        <td class="pnl-percent">-</td>
                        <td>
                            <button class="btn-danger btn-sm" onclick="deleteHolding('${h.symbol}')">Delete</button>
                        </td>
                    </tr>
                `;
            }
        }).join('');
        
        // Update portfolio totals
        const totalPnl = totalCurrentValue - totalCostBasis;
        const totalPnlPercent = totalCostBasis > 0 ? (totalPnl / totalCostBasis * 100) : 0;
        const totalPnlClass = totalPnl >= 0 ? 'positive' : 'negative';
        const totalPnlSign = totalPnl >= 0 ? '+' : '';
        
        document.getElementById('total-current-value').innerHTML = 
            `<strong>$${totalCurrentValue.toFixed(2)}</strong>`;
        document.getElementById('total-pnl').innerHTML = 
            `<strong class="${totalPnlClass}">${totalPnlSign}$${Math.abs(totalPnl).toFixed(2)}</strong>`;
        document.getElementById('total-pnl-pct').innerHTML = 
            `<strong class="${totalPnlClass}">${totalPnlSign}${Math.abs(totalPnlPercent).toFixed(2)}%</strong>`;
        
        // Update last refresh time
        document.getElementById('last-update-time').textContent = new Date().toLocaleTimeString();
        
    } catch (error) {
        showToast('❌ Error loading holdings: ' + error.message, true);
    }
}

// Auto-refresh prices every 30 seconds
let refreshInterval;

function startAutoRefresh() {
    // Load immediately
    loadHoldings();
    
    // Then refresh every 30 seconds
    refreshInterval = setInterval(loadHoldings, 30000);
}

function refreshPrices() {
    loadHoldings();
    showToast('🔄 Prices refreshed!');
}

// Start auto-refresh when holdings tab is active
function showTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Remove active from all buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Show selected tab
    document.getElementById(tabName + '-tab').classList.add('active');
    
    // Activate button
    event.target.classList.add('active');
    
    // Start auto-refresh if holdings tab
    if (tabName === 'holdings') {
        startAutoRefresh();
    } else {
        // Stop auto-refresh for other tabs
        if (refreshInterval) {
            clearInterval(refreshInterval);
        }
    }
}

// Watchlist Management
async function addWatchlistItem(event) {
    event.preventDefault();
    
    const symbol = document.getElementById('watchlist-symbol').value.toUpperCase();
    
    try {
        const response = await fetch('/api/watchlist', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ symbol })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showToast('✅ Added to watchlist!');
            event.target.reset();
            loadWatchlist();
        } else {
            showToast('❌ ' + (data.error || 'Failed to add to watchlist'), true);
        }
    } catch (error) {
        showToast('❌ Error: ' + error.message, true);
    }
}

async function deleteWatchlistItem(symbol) {
    if (!confirm(`Remove ${symbol} from watchlist?`)) {
        return;
    }
    
    try {
        const response = await fetch(`/api/watchlist/${symbol}`, {
            method: 'DELETE'
        });
        
        const data = await response.json();
        
        if (data.success) {
            showToast('✅ Removed from watchlist!');
            loadWatchlist();
        } else {
            showToast('❌ Failed to remove from watchlist', true);
        }
    } catch (error) {
        showToast('❌ Error: ' + error.message, true);
    }
}

async function loadWatchlist() {
    try {
        const response = await fetch('/api/watchlist');
        const watchlist = await response.json();
        
        const container = document.getElementById('watchlist-container');
        container.innerHTML = watchlist.map(symbol => `
            <div class="watchlist-item" data-symbol="${symbol}">
                <span class="symbol-badge">${symbol}</span>
                <button class="btn-danger btn-sm" onclick="deleteWatchlistItem('${symbol}')">×</button>
            </div>
        `).join('');
    } catch (error) {
        showToast('❌ Error loading watchlist', true);
    }
}

// Settings Management
async function updateEmailSettings(event) {
    event.preventDefault();
    
    const emailFrom = document.getElementById('email-from').value;
    const emailTo = document.getElementById('email-to').value;
    
    try {
        const response = await fetch('/api/config', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email_from: emailFrom,
                email_to: emailTo
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showToast('✅ Email settings saved!');
        } else {
            showToast('❌ ' + (data.error || 'Failed to save settings'), true);
        }
    } catch (error) {
        showToast('❌ Error: ' + error.message, true);
    }
}

async function updateStrategySettings(event) {
    event.preventDefault();
    
    const hardStop = parseFloat(document.getElementById('hard-stop').value);
    const warning = parseFloat(document.getElementById('warning').value);
    const profitTarget = parseFloat(document.getElementById('profit-target').value);
    const pullback = parseFloat(document.getElementById('pullback').value);
    const rsiMax = parseFloat(document.getElementById('rsi-max').value);
    
    try {
        const response = await fetch('/api/config', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                hard_stop: hardStop,
                warning: warning,
                profit_target: profitTarget,
                pullback: pullback,
                rsi_max: rsiMax
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showToast('✅ Strategy settings saved!');
        } else {
            showToast('❌ ' + (data.error || 'Failed to save settings'), true);
        }
    } catch (error) {
        showToast('❌ Error: ' + error.message, true);
    }
}

// Auto-uppercase symbol inputs
document.addEventListener('DOMContentLoaded', function() {
    const symbolInputs = document.querySelectorAll('input[pattern="[A-Z]{1,5}"]');
    symbolInputs.forEach(input => {
        input.addEventListener('input', function() {
            this.value = this.value.toUpperCase();
        });
    });
    
    // Start auto-refresh if holdings tab is active on load
    const holdingsTab = document.getElementById('holdings-tab');
    if (holdingsTab && holdingsTab.classList.contains('active')) {
        startAutoRefresh();
    }
});

