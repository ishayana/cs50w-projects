
document.addEventListener('DOMContentLoaded', () => {
    
    const followBtn = document.querySelector('.follow-btn');
    if (followBtn) {

    followBtn.addEventListener('click', function() {
        const userId = this.getAttribute('data-userId');
        following(userId)
    });
    }

    document.querySelectorAll('.edit-post').forEach(button => {
        button.addEventListener('click', (event) => {

            event.preventDefault();
            event.stopPropagation();
            const postId = button.getAttribute('data-postId');
            editPost(postId);
        });
    });
    
    document.querySelectorAll('#save').forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault();
            event.stopPropagation();
            const postId = button.getAttribute('data-postid')
            savePost(postId)
        });
    })
    
    document.querySelectorAll('#cancel').forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault();
            const postId = button.getAttribute('data-postid')
            editCancel(postId)
        });
    })

    document.querySelectorAll('.like-btn').forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault();
            event.stopPropagation();
            const postId = button.getAttribute('data-postId');
            likePost(postId, button)
        })
    })
});


function likePost(postId, button) {
    const csrftoken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    fetch(`like/${postId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify({})

    })
        .then(response => response.json())
        .then(data => {
            const likeCountElement = document.querySelector(`#like-count-${postId}`);
            likeCountElement.innerHTML = `${data.like_count}`;
            if (data.liked) {
                button.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-heart-fill" viewBox="0 0 16 16">
            <path fill-rule="evenodd" d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314"/>
            </svg>
            `;
            } else {
                button.innerHTML = `
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-heart" viewBox="0 0 16 16">
                    <path d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143q.09.083.176.171a3 3 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15"/>
                </svg>
                `;

            }
        })
        .catch(error => console.error('Error:', error));
};

function following(userId) {
    const csrftoken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    fetch(`follow/${userId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify({})
    })
        .then(response => response.json())
        .then(data => {
            const flwBtn = document.querySelector('.follow-btn')
            const flwCount = document.querySelector('#follower-count')
            flwCount.textContent = `${data.follower_count}`
            if (data.followed) {
                flwBtn.textContent = 'Unfollow'
            } else {
                flwBtn.textContent = 'Follow'
            }
        })
        .catch(error => console.error('Error:', error));
}

function editPost(postId) {
    const postTxt = document.querySelector(`#post-text-${postId}`)
    postTxt.style.display = 'none';
    const editForm = document.querySelector(`#edit-form${postId}`)
    editForm.style.display = 'block';
    document.querySelector(`#edit-content-${postId}`).value = postTxt.textContent
}


function savePost(postId) {
    const csrftoken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    const updatedText = document.querySelector(`#edit-content-${postId}`).value
    fetch(`edit/${postId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify({
            text : updatedText
        })
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        };
    })
    .then(data => {
        const postTxt = document.querySelector(`#post-text-${postId}`)
        postTxt.style.display = 'block';
        postTxt.textContent = data.new_text
        const editForm = document.querySelector(`#edit-form${postId}`)
        editForm.style.display = 'none';

    })
}

function editCancel(postId) {
    const postTxt = document.querySelector(`#post-text-${postId}`)
    postTxt.style.display = 'block';
    const editForm = document.querySelector(`#edit-form${postId}`)
    editForm.style.display = 'none';
}