angular.module('InspireApp').controller('AddReportController', function($rootScope, $scope, $http, $timeout) {
    $scope.$on('$viewContentLoaded', function() {
        // initialize core components
        App.initAjax();
        $scope.load_countries();
        $scope.load_metrics();
        $('.date-picker').datepicker({
            autoclose: true,
            clearBtn: true,
            todayHighlight: true
        });
        $scope.load_dimensions();
        $scope.load_ad_units();
    });

    $scope.report = {};
    $scope.dimensions = [];
    $scope.save = function() {
        console.log($scope.report);
        $http({
            method: 'POST',
            url: '/dfp/reports/',
            data: angular.toJson($scope.report)
        });
    };


    $scope.load_dimensions = function() {
        $http({
            method: 'GET',
            url: '/dfp/dimensions'
        }).then(function successCallback(response) {

            $scope.dimensions = response.data.result;
        });
    };

    $scope.load_metrics = function() {
        $http({
            method: 'GET',
            url: '/dfp/metrics'
        }).then(function successCallback(response) {
            $scope.metrics = response.data.result;
        });
    };

    $scope.load_countries = function() {
        $http({
            method: 'GET',
            url: '/dfp/countries'
        }).then(function successCallback(response) {
            $scope.countries = response.data.result;
        });
    };

    $scope.load_ad_units = function() {
        $http({
            method: 'GET',
            url: '/dfp/units'
        }).then(function successCallback(response) {
            $scope.ad_units = response.data.result;
        });
    };
        // set sidebar closed and body solid layout mode
    $rootScope.settings.layout.pageContentWhite = true;
    $rootScope.settings.layout.pageBodySolid = false;
    $rootScope.settings.layout.pageSidebarClosed = false;
});