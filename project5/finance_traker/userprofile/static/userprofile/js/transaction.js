function initTransactionJs() {
    const contentSection = document.querySelector('.page-section');
    const transactionForm = document.querySelector('.createTr-form-container');
    const formTr = document.querySelector('#formTr');
    const formTitle = document.querySelector('.createTr-form > h3');
    const formDescription = document.querySelector('.createTr-form > p');
    const submitBtn = document.querySelector('.submit-tr');
    const tableBody = document.getElementById('transactionTableBody');
    contentSection.addEventListener('click', (event) => {
        console.log('this click for content section!')
        if (event.target.closest('#createTr-btn')) {
            event.stopPropagation()
            transactionForm.classList.remove('hidden');
            
        } else if (event.target.matches('.btn-close')) {
            event.stopPropagation()
            console.log('form should be close')
            transactionForm.classList.add('hidden');
            formTr.reset();
            formTitle.innerHTML = 'Create Your Budget'
            formDescription.innerHTML = 'Take control of your finances by setting up a personalized budget.'
            submitBtn.value = 'Add'
        }
        
        
        if (event.target.closest('.transaction-rm')) {
            event.stopPropagation();
            console.log('clicked on delete button');
            const transactionRm = event.target.closest('.transaction-rm');
            const transactionRow = transactionRm.closest('tr');
            console.log('Adding fade animation to row:', transactionRow);
            transactionRow.classList.add('tr-animate-out')
            const transactionId = transactionRm.getAttribute('data-id');
            setTimeout(() => {
                console.log('Calling deleteTransaction for transactionId:', transactionId);
                deleteTransaction(transactionId);
                transactionRow.remove();
            }, 2000);
        };
        
        
        if (event.target.closest('.transaction-edit')) {
            event.stopPropagation()
            console.log('1')
            const transactionEditBtn = event.target.closest('.transaction-edit')
            const transactionId = transactionEditBtn.getAttribute('data-id')
            updateTransaction(transactionId);
            document.querySelector('#formTr').setAttribute('data-transaction-id', transactionId)
        }
    });


    function formatDate(dateString) {
        const date = new Date(dateString);
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        const hours = String(date.getHours()).padStart(2, '0');
        const minutes = String(date.getMinutes()).padStart(2, '0');
        return `${year}-${month}-${day} ${hours}:${minutes}`;
    }

    fetchTransactionData();
    function fetchTransactionData() {
        fetch('/transaction', {
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
            .then(response => response.json())
            .then(data => {
                const categoryField = document.querySelector('#id_category')
                data.categories.forEach(category => {
                    const option = document.createElement('option')
                    option.value = category.pk
                    option.textContent = category.name
                    categoryField.appendChild(option)
                })
                const transactions = data.transactions;
                const tableBody = document.getElementById('transactionTableBody');
                transactions.forEach((transaction, index) => {
                    const row = document.createElement('tr');
                    row.setAttribute('data-id', `${transaction.id}`)
                    row.innerHTML = `
                    <th class="tr-number" scope="row">${index + 1}</th>
                    <td class="tr-name">${transaction.name}</td>
                    <td class="tr-category">${transaction.category__name}</td>
                    <td class="tr-date">${formatDate(transaction.date)}</td>
                    <td class="tr-amount">
                        ${transaction.transaction_type === 'expense'
                            ? `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" style="color: rgb(150, 0, 0);" class="bi bi-caret-down-fill" viewBox="0 0 16 16">
                                <path d="M7.247 11.14 2.451 5.658C1.885 5.013 2.345 4 3.204 4h9.592a1 1 0 0 1 .753 1.659l-4.796 5.48a1 1 0 0 1-1.506 0z"/>
                              </svg>`
                            : `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" style="color: rgb(0, 150, 70);" class="bi bi-caret-up-fill" viewBox="0 0 16 16">
                                <path d="m7.247 4.86-4.796 5.481c-.566.647-.106 1.659.753 1.659h9.592a1 1 0 0 0 .753-1.659l-4.796-5.48a1 1 0 0 0-1.506 0z"/>
                              </svg>`
                        }
                        ${transaction.amount}
                        
                    </td>
                    <td class='transaction-edit' data-id='${transaction.id}'>
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil-square" viewBox="0 0 16 16">
                        <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"/>
                        <path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5z"/>
                        </svg>
                    </td>
                    <td class='transaction-rm' data-id='${transaction.id}'>
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">
                        <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z"/>
                        <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z"/>
                        </svg>
                    </td>
                `;
                    tableBody.appendChild(row);
                });
            })
            .catch(error => {
                console.error('Error fetching transactions:', error);
            });
    }


    document.querySelector('#formTr').addEventListener('submit', function (event) {
        event.preventDefault();
        const formData = new FormData(this);
        console.log(formData)
        const responseMsg = document.querySelector('#response-message')
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        const transactionId = this.getAttribute('data-transaction-id');
        if (transactionId) {
            fetch(`update_transaction/${transactionId}/`, {
                method: 'PUT',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(Object.fromEntries(formData))
                })
            .then(response => response.json())
            .then(data => {
                if (data.status == 'success') {
                    responseMsg.textContent = data.message;
                    responseMsg.style.backgroundColor = '#D3EFD5'
                    this.reset();
                    transactionForm.classList.add('hidden');
                    row = document.querySelector(`tr[data-id="${transactionId}"]`)
                    rowNum = row.querySelector('.tr-number').textContent

                    row.innerHTML = `
                <th class="tr-number" scope="row">${rowNum}</th>
                <td class="tr-name">${data.transaction.name}</td>
                <td class="tr-category">${data.transaction.category.name}</td>
                <td class="tr-date">${formatDate(data.transaction.date)}</td>
                <td class="tr-amount">
                ${data.transaction.transaction_type === 'expense'
                            ? `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" style="color: rgb(150, 0, 0);" class="bi bi-caret-down-fill" viewBox="0 0 16 16">
                    <path d="M7.247 11.14 2.451 5.658C1.885 5.013 2.345 4 3.204 4h9.592a1 1 0 0 1 .753 1.659l-4.796 5.48a1 1 0 0 1-1.506 0z"/>
                    </svg>`
                            : `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" style="color: rgb(0, 150, 70);" class="bi bi-caret-up-fill" viewBox="0 0 16 16">
                    <path d="m7.247 4.86-4.796 5.481c-.566.647-.106 1.659.753 1.659h9.592a1 1 0 0 0 .753-1.659l-4.796-5.48a1 1 0 0 0-1.506 0z"/>
                    </svg>`
                        }
                ${data.transaction.amount}
                </td>
                <td class='transaction-edit' data-id='${data.transaction.id}'>
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil-square" viewBox="0 0 16 16">
                        <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"/>
                        <path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5z"/>
                        </svg>
                    </td>
                    <td class='transaction-rm' data-id='${data.transaction.id}'>
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">
                        <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z"/>
                        <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z"/>
                        </svg>
                    </td>
                `
                } else {
                    responseMsg.textContent = data.errors;
                    responseMsg.style.backgroundColor = '#EEDBDB'
                }
                responseMsg.style.display = 'block'
                setTimeout(() => {
                    responseMsg.style.display = 'none'
                }, 2000);
                })
                .catch(error => {
                    console.error('Error duting update:', error)
                })



        } else {
            fetch('transaction/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                },
                body: formData
            })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        responseMsg.textContent = data.message;
                        responseMsg.style.backgroundColor = '#D3EFD5'
                        this.reset();
                        const row = document.createElement('tr');
                        const tableBody = document.querySelector('#transactionTableBody')
                        row.setAttribute('data-id', `${data.transaction.id}`)
                        row.innerHTML = `
                    <th class="tr-number" scope="row">${0}</th>
                    <td class="tr-name">${data.transaction.name}</td>
                    <td class="tr-category">${data.transaction.category}</td>
                    <td class="tr-date">${formatDate(data.transaction.date)}</td>
                    <td class="tr-amount">
                    ${data.transaction.transaction_type === 'expense'
                                ? `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" style="color: rgb(150, 0, 0);" class="bi bi-caret-down-fill" viewBox="0 0 16 16">
                        <path d="M7.247 11.14 2.451 5.658C1.885 5.013 2.345 4 3.204 4h9.592a1 1 0 0 1 .753 1.659l-4.796 5.48a1 1 0 0 1-1.506 0z"/>
                        </svg>`
                                : `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" style="color: rgb(0, 150, 70);" class="bi bi-caret-up-fill" viewBox="0 0 16 16">
                        <path d="m7.247 4.86-4.796 5.481c-.566.647-.106 1.659.753 1.659h9.592a1 1 0 0 0 .753-1.659l-4.796-5.48a1 1 0 0 0-1.506 0z"/>
                        </svg>`
                            }
                    ${data.transaction.amount}
                    </td>
                    <td class='transaction-edit' data-id='${data.transaction.id}'>
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil-square" viewBox="0 0 16 16">
                            <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"/>
                            <path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5z"/>
                            </svg>
                        </td>
                        <td class='transaction-rm' data-id='${data.transaction.id}'>
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">
                            <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z"/>
                            <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z"/>
                            </svg>
                        </td>
                    `;
                        if (tableBody.firstChild) {
                            tableBody.insertBefore(row, tableBody.firstChild);
                        } else {
                            tableBody.appendChild(row);
                        }
                    } else {
                        responseMsg.textContent = data.errors;
                        responseMsg.style.backgroundColor = '#EEDBDB'
                    }
                    responseMsg.style.display = 'block'
                    setTimeout(() => {
                        responseMsg.style.display = 'none'
                    }, 2000);
                })
                .catch(error => {
                    console.error('Error on submiting', error)
                })
        }
    })


    function deleteTransaction(transactionId) {
        console.log('one time the dalete transaction perfurm')
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        fetch(`delete_transaction/${transactionId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('Transaction deleted successfully!');
            } else {
                console.log('Somthing went wrong!')
            }
        })
        .catch(error => console.error('Error:', error));
    }


    function updateTransaction(transactionId) {
        fetch(`update_transaction/${transactionId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        })
            .then(response => response.json())
            .then(data => {
                document.querySelector('.createTr-form > h3').innerHTML = 'Update Transaction'
                document.querySelector('.createTr-form > p').innerHTML = 'Please update the details of the transaction below and submit the form.'
                transactionForm.classList.remove('hidden');
                document.querySelector('#id_name').value = data.transaction.name
                document.querySelector('#id_amount').value = data.transaction.amount
                document.querySelector('#id_category').value = data.transaction.category.id
                document.querySelector('#id_transaction_type').value = data.transaction.transaction_type
                if (data.transaction.description === '') {
                    document.querySelector('#id_description').value = ''
                }
                document.querySelector('.submit-tr').value = 'Update'
            })
            .catch(error => {
                console.error('Error:', error)
            })
    };


};