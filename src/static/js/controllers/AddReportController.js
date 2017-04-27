angular.module('InspireApp').controller('AddReportController', function($rootScope, $scope, $http, $state, $stateParams) {

    $scope.is_edit = false;
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
        $('.bs-select').selectpicker();
        $scope.load_dimensions();
        $scope.load_ad_units();
        $scope.initialize_report_options();
    });

    $scope.report = {};
    $scope.step = "1";
    $scope.isDisabled = false;
    $scope.dimensions = [];
    $scope.all_dimensions = [];
    $scope.all_metrics = [];
    $scope.save = function() {
        console.log($scope.report);
        $http({
            method: 'POST',
            url: '/dfp/reports/',
            data: angular.toJson($scope.report)
        }).then(function successCallback(response) {
            $state.go('dashboard');
        });
    };

    if ($stateParams.reportId) {
        $http({
            method: 'HEAD',
            url: '/dfp/report/' + $stateParams.reportId,
            data: angular.toJson($scope.report)
        }).then(function successCallback(response) {
            console.log(response.data.data);
        });
    } else {
        $scope.report = {
            type: 'historical'
        };
    }

    $scope.load_dimensions = function() {
        $http({
            method: 'GET',
            url: '/dfp/dimensions'
        }).then(function successCallback(response) {

            $scope.all_dimensions = response.data.result;
        });
    };

    $scope.load_metrics = function() {
        $http({
            method: 'GET',
            url: '/dfp/metrics'
        }).then(function successCallback(response) {
            $scope.all_metrics = response.data.result;
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


    $scope.initialize_report_options = function() {
        console.log($scope.report.type);
        $scope.dimensions = _.filter($scope.all_dimensions, function(obj){return _.includes(obj.type, $scope.report.type)})
        $scope.metrics = _.filter($scope.all_metrics, function(obj){return _.includes(obj.type, $scope.report.type)})
    };

    $scope.setStep = function(value) {
        if (value == '3' && $scope.report.type != 'sale') {
            $scope.save()
        } else {
            $scope.step = value
        }
        console.log($scope.report);
    };

    $rootScope.settings.layout.pageContentWhite = true;
    $rootScope.settings.layout.pageBodySolid = false;
    $rootScope.settings.layout.pageSidebarClosed = false;
});