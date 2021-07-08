document.addEventListener('DOMContentLoaded', function() {
  console.log('loaded');

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

  // Sends email
  document.querySelector('#compose-form').onsubmit = function() {
    console.log('thing clicked');
    const formRecipient = document.querySelector('#compose-recipients').value;
    const formSubject = document.querySelector('#compose-subject').value;
    const formBody = document.querySelector('#compose-body').value;
    send_mail(formRecipient, formSubject, formBody);
    return false;
  };

});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  console.log('composing');
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Load emails based on mailbox view
  loadEmails(mailbox);
  
}

function send_mail(formRecipient, formSubject, formBody){


  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: formRecipient,
        subject: formSubject,
        body: formBody,
    })
  })
  .then(response => response.json())
  .then(result => {
      load_mailbox('inbox');
  })
  .catch(error => {
    console.log('Error:', error);
  });
}

function loadEmails(mailbox){
  fetch('/emails/' + mailbox)
  .then(response => response.json())
  .then(emails => {
    populateEmails(emails);
  })
  .catch(error=>{
    console.log('Error:', error);
  });

};


function populateEmails(emails){
  // Create main list div
  let mailList = document.createElement('div');
  document.querySelector('#emails-view').appendChild(mailList);
  
  // Styling for each mail div
  const divStyle = {
    display: 'flex',
    flexDirection: 'row',
    justifyContent: 'space-between',
    border: 'solid',
    borderWidth: '1px',
    margin: '10px',
    padding: '10px',
  }

  // Load all emails
  for (let i = 0; i < emails.length; i++){
    // Main div box
    const mailDiv = document.createElement('div');
    const mailID = emails[i].id;
    Object.assign(mailDiv.style, divStyle);

    // Gray style if unread 
    if (!emails[i].read){
      mailDiv.style.backgroundColor = '#e5e5e5';
    }

    // Half holds sender/subject
    const firstHalfDiv = document.createElement('div');
    firstHalfDiv.style.display = 'flex';
    firstHalfDiv.style.flexDirection = 'row';

    const emailDiv = document.createElement('div');
    emailDiv.style.fontWeight = 'bold';
    emailDiv.innerHTML = emails[i].sender;

    const subjectDiv = document.createElement('div');
    subjectDiv.innerHTML= emails[i].subject;
    subjectDiv.style.paddingLeft = '10px';

    firstHalfDiv.appendChild(emailDiv);
    firstHalfDiv.appendChild(subjectDiv);
    
    const timeDiv = document.createElement('div');
    timeDiv.innerHTML= emails[i].timestamp;
    timeDiv.style.textAlign= 'right';

    
    mailDiv.appendChild(firstHalfDiv);
    mailDiv.appendChild(timeDiv);
    mailList.appendChild(mailDiv);

    // Click > opens email 
    mailDiv.addEventListener('click', () => {
      loadEmail(mailID);
      return false;
    })
  }
}

function loadEmail(mailID){
  // Styling for individual mail load
  const divStyle = {
    display: 'flex',
    flexDirection: 'column',
    margin: '10px',
    padding: '10px',
  }

  const ID = parseInt(mailID);
  fetch('/emails/' + ID)
  .then(response => response.json())
  .then(emails => {
      console.log(emails);
      // Mark as read
      fetch(('/emails/' + ID), {
        method: 'PUT',
        body: JSON.stringify({
            read: true
        })
      })
      // Clear existing DOMs 
      document.querySelector('#emails-view').textContent='';

      // Create main div
      let mailDiv = document.createElement('div');
      document.querySelector('#emails-view').appendChild(mailDiv);
      Object.assign(mailDiv.style, divStyle);

      // Load information 
      let sender = document.createElement('div');
      sender.innerHTML= `From: ${emails.sender}`;

      let recipients = document.createElement('div');
      recipients.innerHTML = `To: ${emails.recipients}`;

      let subject = document.createElement('div');
      subject.innerHTML = `Subject: ${emails.subject}`;

      let timestamp = document.createElement('div');
      timestamp.innerHTML = `Timestamp: ${emails.timestamp}`; 

      let reply = document.createElement('button');
      reply.textContent = "Reply";
      reply.className= "btn btn-sm btn-outline-primary";
      reply.style.width = "120px";

      reply.addEventListener('click', () => {
        compose_reply(ID);
        return false;
      })

      let separator = document.createElement('hr');
      separator.style.size = '3px';
      separator.style.width = '100%';
      separator.style.color = "black";

      let body = document.createElement('div');
      body.innerHTML = emails.body;

      let archive = document.createElement('button');
      archive.textContent = "Archive";
      archive.className= "btn btn-sm btn-outline-primary";
      archive.style.width = "150px";
      archive.style.marginTop = "25px";
      archive.style.float = "right";

      archive.addEventListener('click', () => {
        // Mark as read
        fetch(('/emails/' + ID), {
        method: 'PUT',
        body: JSON.stringify({
          archived: true
          })
        })
        load_mailbox('inbox');
        return false;
      })


      mailDiv.appendChild(sender);
      mailDiv.appendChild(recipients);
      mailDiv.appendChild(subject);
      mailDiv.appendChild(timestamp);
      mailDiv.appendChild(reply);
      mailDiv.appendChild(separator);
      mailDiv.appendChild(body);
      mailDiv.appendChild(archive);


  });
}

function compose_reply(ID){
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Preload out composition fields
  fetch('/emails/' + ID)
  .then(response => response.json())
  .then(emails => {
    document.querySelector('#compose-recipients').value = emails.sender;
    document.querySelector('#compose-subject').value = emails.subject;
    document.querySelector('#compose-body').value = `On ${emails.timestamp} ${emails.sender} wrote: ${emails.body}`;
  })
}