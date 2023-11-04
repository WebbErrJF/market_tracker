document.addEventListener('DOMContentLoaded', () => {
        const messageInputDom = document.querySelector('#chat-message-input');
        const messageSubmitButton = document.querySelector('#chat-message-submit');

        messageInputDom.focus();

        messageInputDom.onkeyup = function (e) {
            if (e.key === 'Enter') {
                messageSubmitButton.click();
            }
        };
});

function openDeleteModal(commentId) {
        const modal = document.getElementById("ModalDelete_" + commentId);
        const modal_close = document.getElementById("modal_close_" + commentId);

        modal.style.display = "block";

        window.onclick = function(event) {
            if (event.target == modal) {
                modal.style.display = "none";
            }
        }

        modal_close.onclick = function() {
          modal.style.display = "none";
        }
    }

function openModal(commentId) {
        const modal = document.getElementById("Modal_" + commentId);
        const span = document.getElementById("close_" + commentId);
        const textarea = document.getElementById("modal-text-box_" + commentId);
        const commentContent = document.getElementById(commentId).textContent;

        modal.style.display = "block";
        textarea.value = commentContent;

        window.onclick = function(event) {
            if (event.target == modal) {
                modal.style.display = "none";
            }
        }

        span.onclick = function() {
          modal.style.display = "none";
          textarea.value = "";
        }
    }

function addComment(article_id) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const textarea = document.getElementById("chat-message-input");
    const value = textarea.value;

    $.ajax({
            url: '/comment/',
            type: 'POST',
            headers: { 'X-CSRFToken': csrftoken },
            data: { content: value,
                    article_id: article_id
                    },
            success: function(response) {
                location.reload();
            },
            error: function(error) {
                console.error('Error POST:', error);
            }
        });
    textarea.value = '';
}

function deleteComment(commentId) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $.ajax({
            url: '/comment/' + commentId + '/',
            type: 'DELETE',
            headers: { 'X-CSRFToken': csrftoken },
            success: function(response) {
                const comment_section = document.getElementById("single_comment_section_" + commentId);
                const modal = document.getElementById("Modal_" + commentId);
                const modalDelete = document.getElementById("ModalDelete_" + commentId);
                modalDelete.style.display = "none";
                modalDelete.remove()
                modal.remove();
                comment_section.remove();
            },
            error: function(error) {
                console.error('Error DELETE:', error);
            }
        });

}

function editComment(commentId) {
    const textarea = document.getElementById("modal-text-box_" + commentId);
    const value = textarea.value;
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    $.ajax({
            url: '/comment/' + commentId + '/',
            type: 'PATCH',
            data: { content: value },
            headers: { 'X-CSRFToken': csrftoken },
            success: function(response) {
                const commentId = response.id;
                const newContent = response.content;
                const pElement = document.getElementById(commentId);
                pElement.innerHTML = newContent;

                const dateElement = document.getElementById("date_" + commentId);
                const newDate = response.date_posted;
                dateElement.innerHTML = newDate;

                const modal = document.getElementById("Modal_" + commentId);
                modal.style.display = "none";
            },
            error: function(error) {
                console.error('Error PATCH:', error);
                const modal = document.getElementById("Modal_" + commentId);
                modal.style.display = "none";
            }
        });
}