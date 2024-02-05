$(document).ready(function () {
    $("#categoryForm").submit(function (e) {
        e.preventDefault();

        $.ajax({
            type: 'POST',
            url: '/mypage/new_review_ajax/',
            data: $(this).serialize(),
            success: function (response) {
                console.log(response.predict_result);

                // Update the content and make the element visible
                $("#prediction_result").html("고객님이 입력하신 리뷰의 예측 별점은" + response.predict_result + "입니다.").show();
            },
            error: function (error) {
                console.log(error);
            }
        });
    });
});
