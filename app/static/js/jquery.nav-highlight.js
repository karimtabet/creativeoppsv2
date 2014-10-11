$(window).scroll(function() {
    var height = $(window).scrollTop();
    var projectsPosition = $(projects).offset();
    var contactPosition = $(contact).offset();

    if(height  < 300) {
        $("#homeBtn").addClass("pure-menu-selected");
        removeClass("#projectsBtn", "#contactBtn");
    } 
    if (height  > projectsPosition.top - 300) {
        $("#projectsBtn").addClass("pure-menu-selected");
        removeClass("#homeBtn", "#contactBtn");
    } 
    if (height  > contactPosition.top - 300) {
        $("#contactBtn").addClass("pure-menu-selected");
        removeClass("#homeBtn", "#projectsBtn");
    }
});

function removeClass(button1, button2) {
    $(button1).removeClass("pure-menu-selected");
    $(button2).removeClass("pure-menu-selected");
}