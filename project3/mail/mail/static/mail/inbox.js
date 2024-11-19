document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').addEventListener('submit', send_mail);
  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#email-detail').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  fetch(`emails/${mailbox}`)
  .then(Response => Response.json())
  .then(emails => {
    console.log(emails);
    
    // Show the mailbox and hide other views
    document.querySelector('#emails-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#email-detail').style.display = 'none';
    
    // Show the mailbox name

    
    document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>
    <table class="table table-hover">
    <thead>
    <tr>
    <th scope="col" class="sender-inbox">Sender</th>
    <th scope="col" class="subject-inbox">Subject</th>
    <th scope="col" class="timestamp-inbox">Timestamp</th>
    </tr>
    </thead>
    <tbody id="emails-tbody">
    </tbody>
    </table>
    `;
    const emailsTbody = document.querySelector('#emails-tbody');
    if (emails.length === 0) {
      const alert = document.createElement('div');
      alert.innerHTML = 'No emails!'
      emailsTbody.appendChild(alert)
    } else{

      emails.forEach(email => {
        const rowMail = document.createElement('tr');
        rowMail.className = email.read ? 'row-mail read' : 'row-mail';
        rowMail.classList.add('row-mail')
        rowMail.innerHTML = `
        <td>${email.sender}</td>
        <td>${email.subject}</td>
        <td>${email.timestamp}</td>
        `;
        rowMail.addEventListener('click', () => emailDetails(email.id));
        emailsTbody.appendChild(rowMail);
      });
    }
  })
  .catch(error => console.error('error fechin '))
  }


// Send emails
function send_mail(event) {
  event.preventDefault();
  console.log('send mail function perfurm')
  const recipientsValue = document.querySelector('#compose-recipients').value;
  const subjectValue = document.querySelector('#compose-subject').value;
  const bodyValue = document.querySelector('#compose-body').value;
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: recipientsValue,
      subject: subjectValue,
      body:bodyValue
    })
  })
    .then(response => response.json())
    .then(result => {
      console.log(result)
      load_mailbox('sent');
  });
  
  
};


// Get mail
function emailDetails(id) {
  document.querySelector('#emails-view').style.display = 'none'
  document.querySelector('#email-detail').style.display = 'block'
  fetch(`emails/${id}`, {
    method:'PUT',
    body: JSON.stringify({
      read: true
    })
  })
  fetch(`emails/${id}`)
  .then(Response => Response.json())
  .then(email => {
    const formattedBody = email.body.replace(/\n/g, '<br>');
    document.querySelector('#email-detail').innerHTML = 
    `<button id='reply-btn' class="btn btn-outline-primary">Reply</button>
    <button id='archive-btn' class="btn btn-outline-success">${email.archived ? 'Unarchive' : 'Archive'}</button>
    <br>
    <p><b>Sender:</b> <span>${email.sender}</span></p>
    <p><b>Recipients:</b> <span>${email.recipients}</span></p>
    <p><b>Timestamp:</b> <span>${email.timestamp}</span></p>
    <p><b>Subject:</b> <span>${email.subject}</span></p>
    <hr>
    <p><span>${formattedBody}</span></p>
    `;
    document.querySelector('#reply-btn').addEventListener('click', () => emailReply(email))
    document.querySelector('#archive-btn').addEventListener('click', () => emailArchive(email))
  })
}


function emailArchive(email) {
  const archiveStatus = !email.archived;
  fetch(`emails/${email.id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: archiveStatus
    }),
    headers: {
      'Content-Type': 'application/json'
    }
  })
  .then(response => {
    document.querySelector('#archive-btn').innerHTML = archiveStatus ? 'Unarchive' : 'Archive'
    email.archived = archiveStatus
    console.log(`archived :   ${archiveStatus}`)
  })
}

function emailReply(email) {
  document.querySelector('#email-detail').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#compose-recipients').value = email.sender;
  document.querySelector('#compose-subject').value = email.subject;
  if (!(email.subject.substring(0, 4) === 'Re: ')) {
    document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
  }
  document.querySelector('#compose-body').value = `
  
  
  ____________________________________________________
  On ${email.timestamp} ${email.sender} wrote:
  ${email.body}`;

}




