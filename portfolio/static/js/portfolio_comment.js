const modifyNewComment = (portfolio_id, comment_id, value) => {
    console.log(portfolio_id, comment_id, value);
    const commentContainer = document.querySelector(`.comments-${portfolio_id}`);
    console.log(commentContainer)

    const tempContainer = document.createElement("div");
    tempContainer.className = `comment comments-${comment_id}`;


    tempContainer.textContent = value;

    const deleteBtn = document.createElement("input");
    deleteBtn.className = "comment-btn";
    deleteBtn.setAttribute("type", "submit");
    deleteBtn.setAttribute("value", "삭제");
    deleteBtn.setAttribute("onclick", `onClickDeleteComment(${comment_id})`)

    tempContainer.appendChild(deleteBtn);
    commentContainer.appendChild(tempContainer);

}

const onClickNewComment = async (id) => {
    try{
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
    }   catch (error) {
        console.log(error)
    }
    
}

const modifyDeleteComment = (comment_id) => {

    const targetCommentContainer = document.querySelector(`.comments-${comment_id}`);
    console.log(targetCommentContainer)
    targetCommentContainer.remove();
}

const onClickDeleteComment = async (commentId) => {
    const url = `/portfolio/comment_delete/`;

    const {
        data
    } = await axios.post(url, {
        commentId
    })
    modifyDeleteComment(data.comment_id);
}