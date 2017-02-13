angular.module('InspireApp').controller('AddReportController', function($rootScope, $scope, $http, $timeout) {
    $scope.$on('$viewContentLoaded', function() {
        // initialize core components
        App.initAjax();
        $http({
            method: 'GET',
            url: '/dfp/countries'
        }).then(function successCallback(response) {
            console.log(response.data.result);
            $scope.countries = response.data.result;
        });
    });

    $scope.report = {}
    $scope.save = function(report){
        console.log(report);

    }

        // set sidebar closed and body solid layout mode
    $rootScope.settings.layout.pageContentWhite = true;
    $rootScope.settings.layout.pageBodySolid = false;
    $rootScope.settings.layout.pageSidebarClosed = false;
});