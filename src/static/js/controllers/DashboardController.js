angular.module('InspireApp').controller('DashboardController', function($rootScope, $scope, $http, $timeout) {
    $scope.$on('$viewContentLoaded', function() {
        // initialize core components
        App.initAjax();
        $http({
            method: 'GET',
            url: '/dfp/reports'
        }).then(function successCallback(response) {
            $scope.reports = response.data.result;
        });
    });

    $scope.delete_report = function(report) {
            $http({
                method: 'DELETE',
                url: '/dfp/report/' + report.id
            }).then(function successCallback(response) {
                if (response.data.result == 'success') {
                    var index = $scope.reports.indexOf(report);
                    $scope.reports.splice(index, 1);
                } else {
                    alert('Delete was unsuccessful');
                }

            });
        }
        // set sidebar closed and body solid layout mode
    $rootScope.settings.layout.pageContentWhite = true;
    $rootScope.settings.layout.pageBodySolid = false;
    $rootScope.settings.layout.pageSidebarClosed = false;
});