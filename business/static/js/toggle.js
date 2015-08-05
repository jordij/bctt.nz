// Wait until the DOM is loaded, before trying to query the document
$(document).ready(function(){

  // select the .head elements, and bind an event handler to them
  $('.toggle-btn').click(function(e){

    // prevent the default action of the click event
    // ie. prevent the browser from redirecting to the link's href
    e.preventDefault();

    // 'this' is the execution context of the event handler
    // it refers to the clicked .head element
    $(this)

    // Walk up the DOM tree to find the closest list item
    // It is the closest shared ancestor of both .head and .content
    .closest('li')

    // Search the list item for .content
    .find('.toggle-content')

    // Trigger the sliding animation on .content
    .slideToggle();
  });
});