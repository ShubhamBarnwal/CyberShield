$("#analyze_text").on("click", function(){
    // Take the contents of the textarea with ID comment_query and assign it to the
    // comment_text variable
    var comment_text = $("#comment_query").val();

    // Validate that the comment_text is not empty; if it is, then return false to quit the submission immediately
    if (comment_text.length <= 0) return false;

    // The comment appears to be present; we will, as such, send the AJAX request here
    $.ajax({
        url: 'analyze',               // The URL endpoint is @ /analyze
        method: 'POST',               // For now we will send a POST request with the data
        data: {'text': comment_text}, // Send a data object, storing the comment text in a 'text' parameter
        beforeSend: function(){
            // This code will run before the request is sent to our Python Code
            $("#loader").fadeIn();
        },
        success: function(response){

            $("#loader").fadeOut();

            $("#results").html("");

            // Add the full prediction set to the list
            response['classes'].forEach(function(element, index) {
                // This loops through each of the class elements;
                // index is the number 0..5 that corresponds to the given class
                $("#results").append(
                    "<a class='list-group-item'>"+ // Add a list item anchor tag to the list
                    element['class_name']+      // Include the text of the class name
                    " ("+                       // In brackets include the confidence %
                    (element['confidence']*100).toFixed(2)+
                    "%)</a>");
            });

            // Scroll the page to the top of the holder so that the user can see the results immediately
            $(window).scrollTop($("#results").offset().top);

        }
    });

    // Return false prevents the default behaviour from engaging (i.e. the button will not actually submit the contents
    // in the typical manner, since we have already handled the form submission)
    return false;
});