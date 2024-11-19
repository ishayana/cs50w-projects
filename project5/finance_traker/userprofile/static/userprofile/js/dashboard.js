function initDashboardJs() {
    const contentSection = document.querySelector('.page-section');
    const formBg = document.querySelector('#formbg');

    
    contentSection.addEventListener('click', (event) => {
        const bugetForm = document.querySelector('.createbg-form-container');
        
        if (event.target.closest('#createbg-btn')) {
            bugetForm.classList.remove('hidden');
        } else if(event.target.matches('.btn-close')) {
            bugetForm.classList.add('hidden');
        }
    });

    let myChart;

    fetchDashboardData();
    function fetchDashboardData(){
        fetch('/dashboard',{
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            document.querySelector('.balance > h4').textContent = `$${data.balance}`;
            document.querySelector('.income > h4').textContent = `$${data.total_income}`;
            document.querySelector('.expense > h4').textContent = `$${data.total_expense}`;
            const noChartAlert = document.querySelector('#nochart-alert')
            const ctx = document.getElementById('myChart');
            myChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: data.labels,
                datasets: [{
                label: 'Budget',
                data: data.datasets[0].data,
                backgroundColor: [
                    "#bcdde6",
                    "#9dd7e6",
                    "#b2dfeb",
                    "#62bed9",
                    "#5da7ba",
                    "#578e9b",
                    "#4e757e",
                    "#475e64",
                    "#3d4748",
                    "#33322e"
                ],
                borderWidth: 1
                }]
            }, 
            options: {
                legend: false,
                responsive: true,
                scales: {
                y: {
                    display: false,
                    beginAtZero: false
                },
                }
            }
            });
            if (!data.labels || data.labels.length === 0){
                noChartAlert.classList.remove('hidden')
                ctx.style.display = 'none';
            }

        })
        .catch(error => {
            console.error('Error fetching dashboard data:', error);
        });
    }

    
    document.querySelector('#formbg').addEventListener('submit', function(event) {
        event.preventDefault();
        const responseMsg = document.querySelector('#response-message')
        const formData = new FormData(this)
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        fetch('dashboard/', {
            method: 'POST',
            body: formData,
            headers:{
                'X-CSRFToken': csrfToken
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                document.querySelector('.balance > h4').textContent = `$${data.new_balance}`;
                
                responseMsg.textContent = 'Feedback submitted successfully!';
                responseMsg.style.backgroundColor = '#D3EFD5'
                this.reset();
                myChart.data.datasets[0].data.push(data.amount);
                myChart.data.labels.push(data.category);
                myChart.update();
            } else {
                responseMsg.textContent = 'Error: ' + JSON.stringify(data.errors.category[0]);
                responseMsg.style.backgroundColor = '#EEDBDB'
            }
            responseMsg.style.display = 'flex'
            setTimeout(() => {
                responseMsg.style.display = 'none'
            }, 2000);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    

};
     
