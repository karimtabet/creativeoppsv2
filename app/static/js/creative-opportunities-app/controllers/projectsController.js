app.controller("projectsController", function($scope, $http) {
    $scope.project = {};
    $scope.projectList = [];
    $scope.project.photos = [];
    $scope.project.videos = [];
    var projectIndex = 0;
    $scope.init = function() {
        //necessary for cross domain request
        delete $http.defaults.headers.common['X-Requested-With'];

        var url = 'https://spreadsheets.google.com/feeds/list/1JUi43YqJF5tkkRszQnJSdiGSdoxKeG699pqgB272Pu4/od6/public/basic?hl=en_US&alt=json'
        $http.get(url).success(function(data) {
            var entry = data.feed.entry;
            angular.forEach(entry, function(value, index) {
                var title = value.title.$t;
                var content = value.content.$t.substring(9);
                switch (title) {
                    case "Title":
                        $scope.project = {};
                        $scope.project.id = projectIndex;
                        $scope.project.photos = [];
                        $scope.project.videos = [];
                        $scope.project.title = content;
                    case "Dates":
                        $scope.project.dates = content;
                    case "Location":
                        $scope.project.location = content;
                    case "Description":
                        $scope.project.description = content;
                }
                if (title == "Video") {
                    $scope.project.videos.push(content);
                } else if (title == "Photo") {
                    $scope.project.photos.push(content);
                }
                if (title == "END PROJECT") {
                    $scope.projectList.push($scope.project);
                    projectIndex += 1;
                }
            });
        }).error(function(error) {
 
        });
    };

});

