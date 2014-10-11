app.controller("mainContentController", function($scope, $http) {
    $scope.init = function() {
        //necessary for cross domain request
        delete $http.defaults.headers.common['X-Requested-With'];

        var url = 'https://spreadsheets.google.com/feeds/list/15oREoh6Csjn3cidwUcAczqbtZ882EwD1Qrh1jUnXKjc/od6/public/basic?hl=en_US&alt=json'
        $http.get(url).success(function(data) {
            var entry = data.feed.entry
            angular.forEach(entry, function(value, index) {
                var content = value.content.$t.substring(9)
                switch (value.title.$t) {
                    case "Home":
                        $scope.home = content;
                    case "Splash Video":
                        $scope.video = content;
                    case "Projects":
                        $scope.projects = content;
                    case "Contact":
                        $scope.contact = content;
                }
                if (value.title.$t == "Contact Text 1") {
                    $scope.con_text_1 = content;
                }
                if (value.title.$t == "Contact Name 1") {
                    $scope.con_name_1 = content;
                }
                if (value.title.$t == "Contact Photo 1") {
                    $scope.con_photo_1 = content;
                }
                if (value.title.$t == "Contact Text 2") {
                    $scope.con_text_2 = content;
                }
                if (value.title.$t == "Contact Name 2") {
                    $scope.con_name_2 = content;
                }
                if (value.title.$t == "Contact Photo 2") {
                    $scope.con_photo_2 = content;
                }
                if (value.title.$t == "Contact Text 3") {
                    $scope.con_text_3 = content;
                }
                if (value.title.$t == "Contact Name 3") {
                    $scope.con_name_3 = content;
                }
                if (value.title.$t == "Contact Photo 3") {
                    $scope.con_photo_3 = content;
                }
        });
        }).error(function(error) {
 
        });
    };

});

