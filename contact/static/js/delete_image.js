function remove(el) {
    var element = el;
    //I have also tried using document.getElementByID(this.id)
    element.parentNode.remove();
    //I have also tried using element.parentNode.removeChild(element); to remove the element.
  }