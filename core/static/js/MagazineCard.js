import "../css/MagazineCard.css";

function MagazineCard({ img, title, user, meta, width, height }) {
    return (
      <div
        className="MagazineCard"
        style={{ width: width || 247, height: height || 337 }}
        draggable
      >
        <div className="image_container">
          <img src={img} alt="random magazine" />
        </div>
  
        <div className="info_container">
          <h2 className="title">{title}</h2>
  
          <div className="user_container">
            <span className="username">{user.name}</span>
            <div className="user_category">{user.category}</div>
          </div>
  
          <div className="meta_container">
            <div className="like">
              <i className="fas fa-heart"></i>
              {meta.like}
            </div>
            <div className="view">
              <i className="fas fa-eye"></i>
              {meta.view}
            </div>
            <div className="bookmark">
              <i className="fas fa-bookmark"></i>
              {meta.bookmark}
            </div>
          </div>
        </div>
      </div>
    );
  }