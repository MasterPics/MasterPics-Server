const modifyNewComment = (portfolio_id, comment_id, value) => {
    const CommentContainer = document.querySelector(`.comments-${portfolio_id}`);

    const tempContainer = document.createElement("div");
    tempContainer.className = `comment comment-${comment_id}`;


    /* comment wrapper */

    const commentWrapper = document.createElement("div");
    commentWrapper.className = 'comment__wrapper';
    commentWrapper.innerHTML = `<div class="comment__item">` +
        `<div class="comment__writer-img">` +
        `<img src="${userImage}">` +
        `</div>` +
        `<div class="comment__content">` +
        `<div class="comment__top-info">` +
        `<span class="comment__writer">${writer}</span>` +
        `<span class="comment__date">` + "방금 전" + `</span>` +
        `</div>` +
        `<span class="comment__text">${value}</span>` +
        `</div>` +
        `</div>` +
        `<input class="comment__delete-btn comment-btn" onclick="onClickDeleteComment(${comment_id})" type="submit" value="삭제">`;


    CommentContainer.appendChild(tempContainer);
    tempContainer.appendChild(commentWrapper);

    /* 가장 위에 최신 댓글 삽입 */
    CommentContainer.insertBefore(tempContainer, CommentContainer.firstChild);
}

const onClickNewComment = async (id) => {
    try {
        const url = `/portfolio/comment_create/`;
        const value = document.querySelector(`.createComment-${id} .comment__value`);
        const value_text = value.value
        const {
            data
        } = await axios.post(url, {
            id,
            value: value_text
        })

        modifyNewComment(id, data.comment_id, data.value);

        const cmt = document.querySelector('.comment__value')
        cmt.value = ''
    } catch (error) {
        console.log(error)
    }

}

const modifyDeleteComment = (comment_id) => {

    const targetCommentContainer = document.querySelector(`.comment-${comment_id}`);
    targetCommentContainer.remove();
}

const onClickDeleteComment = async (commentId) => {
    if (confirm("댓글을 삭제하시겠습니까?")) {
        const url = `/portfolio/comment_delete/`;

        const {
            data
        } = await axios.post(url, {
            commentId
        })
        modifyDeleteComment(data.comment_id);
    } else {
        return;
    }
}