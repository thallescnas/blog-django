const el = document.getElementById('dados-mes');
if (el) {
    const dados = JSON.parse(el.textContent);
    new Chart(document.getElementById('graf-mes'), {
        type: 'bar',
        data: {
            labels: dados.map(d => d.mes),
            datasets: [{
                label: 'Posts por mês',
                data: dados.map(d => d.total),
                backgroundColor: '#4f46e5',
                borderRadius: 6,
            }]
        },
        options: {
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { precision: 0 }
                }
            }
        }
    });
}
