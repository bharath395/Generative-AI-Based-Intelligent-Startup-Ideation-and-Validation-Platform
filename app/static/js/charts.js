let validationRadarChart = null;
let marketGrowthChart = null;
let domainBarChart = null;

function renderValidationChart(canvasId, scores) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return;

  if (validationRadarChart) validationRadarChart.destroy();

  validationRadarChart = new Chart(ctx, {
    type: 'radar',
    data: {
      labels: ['Innovation (25%)', 'Market Demand (30%)', 'Tech Possibility (25%)', 'Profitability (20%)'],
      datasets: [{
        label: 'Startup Score Breakdown',
        data: [scores.innovation || 90, scores.market || 85, scores.technology || 80, scores.business || 88],
        backgroundColor: 'rgba(37, 99, 235, 0.25)',
        borderColor: '#2563EB',
        pointBackgroundColor: '#7C3AED',
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: '#7C3AED'
      }]
    },
    options: {
      responsive: true,
      scales: {
        r: {
          angleLines: { color: 'rgba(148, 163, 184, 0.2)' },
          grid: { color: 'rgba(148, 163, 184, 0.2)' },
          suggestedMin: 0,
          suggestedMax: 100
        }
      }
    }
  });
}

function renderMarketTrendChart(canvasId, domainName = 'Market', customLabels = null, customData = null) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return;

  if (marketGrowthChart) marketGrowthChart.destroy();

  const labels = customLabels || ['2023', '2024', '2025', '2026', '2027 (Est)', '2028 (Est)'];
  const data = customData || [4.2, 5.8, 8.1, 12.4, 16.8, 22.5];

  marketGrowthChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: `${domainName} Growth Valuation (₹ Cr)`,
        data: data,
        borderColor: '#10B981',
        backgroundColor: 'rgba(16, 185, 129, 0.15)',
        pointBackgroundColor: '#2563EB',
        fill: true,
        tension: 0.35

      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: true } }
    }
  });
}


function renderDomainDistributionChart(canvasId, labels, data) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return;

  if (domainBarChart) domainBarChart.destroy();

  const palette = ['#2563EB', '#10B981', '#7C3AED', '#F59E0B', '#06B6D4', '#EC4899', '#6366F1', '#14B8A6'];
  const chartLabels = (labels && labels.length > 0) ? labels : ['No Saved Ideas Yet'];
  const chartData = (data && data.length > 0) ? data : [0];
  const bgColors = chartLabels.map((_, idx) => palette[idx % palette.length]);

  domainBarChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: chartLabels,
      datasets: [{
        label: 'Number of Startup Ideas',
        data: chartData,
        backgroundColor: bgColors,
        borderRadius: 8
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: function(context) {
              const val = context.parsed.y;
              return ` ${val} ${val === 1 ? 'Startup Idea' : 'Startup Ideas'}`;
            }
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'Number of Ideas'
          },
          ticks: {
            precision: 0,
            stepSize: 1
          }
        },
        x: {
          title: {
            display: true,
            text: 'Domain Category'
          }
        }
      }
    }
  });
}


