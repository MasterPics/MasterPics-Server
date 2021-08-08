import MagazineCard from "./MagazineCard";

const cards = [
    {
      img:
        "https://images.unsplash.com/photo-1596760020480-3b330a990539?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=935&q=80",
      title: "This is TITLE",
      user: {
        name: "Seol",
        category: "photographer",
      },
      meta: {
        like: 213,
        view: 12123,
        bookmark: 123,
      },
    },
    {
      img:
        "https://images.unsplash.com/photo-1616740386718-6a4e42e3cf02?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80",
      title: "This is TITLE",
      user: {
        name: "Seol",
        category: "photographer",
      },
      meta: {
        like: 213,
        view: 12123,
        bookmark: 123,
      },
    },
    {
      img:
        "https://images.unsplash.com/photo-1615537572530-4c76817865c6?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80",
      title: "This is TITLE",
      user: {
        name: "Seol",
        category: "photographer",
      },
      meta: {
        like: 213,
        view: 12123,
        bookmark: 123,
      },
    },
    {
      img:
        "https://images.unsplash.com/photo-1614788466123-1ec2a5833087?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80",
      title: "This is TITLE",
      user: {
        name: "Seol",
        category: "photographer",
      },
      meta: {
        like: 213,
        view: 12123,
        bookmark: 123,
      },
    },
    {
      img:
        "https://images.unsplash.com/photo-1618278096912-d14cda36d45b?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1651&q=80",
      title: "This is TITLE",
      user: {
        name: "Seol",
        category: "photographer",
      },
      meta: {
        like: 213,
        view: 12123,
        bookmark: 123,
      },
    },
  ];


document.getElementsByClassName("RandomMagazine")= function RandomMagazine() {
    cards.map((card, index) => {
    return (
      <div className={`card_container-${index}`}>
        <MagazineCard key={index} {...card} />
      </div>
    );
  })}