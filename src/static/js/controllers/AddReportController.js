angular.module('InspireApp').controller('AddReportController', function($rootScope, $scope, $http, $state, $stateParams, $q) {

    $scope.is_edit = false;


    $scope.report = {};
    $scope.step = "1";
    $scope.isDisabled = false;
    $scope.dimensions = [];
    $scope.communities = [];
    $scope.metrics = [];

    function create_new_report() {
        var report = {
            "type": 'sale',
            "metrics": _.filter($scope.metrics, {
                'default': true
            }),
            "country": _.find($scope.countries, {'id':'US'})
        };
        console.log(report);
        return report;
    };

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

    function load_dimensions() {
        return $http({
            method: 'GET',
            url: '/dfp/dimensions'
        }).then(function successCallback(response) {
            $scope.dimensions = response.data.result;
        });
    }

    function load_metrics() {
        return $http({
            method: 'GET',
            url: '/dfp/metrics'
        }).then(function successCallback(response) {
            console.log('done metrics');
            $scope.metrics = response.data.result;
        });
    };

    function load_countries() {
        return $http({
            method: 'GET',
            url: '/dfp/countries'
        }).then(function successCallback(response) {
            $scope.countries = response.data.result;
        });
    };

    function load_communities() {
        return $http({
            method: 'GET',
            url: '/dfp/communities'
        }).then(function successCallback(response) {
            $scope.communities = response.data.result;
        });
    };

    function initialize_report(){
        console.log($scope.report.type);
        if ($stateParams.reportId) {
            $http({
                method: 'HEAD',
                url: '/dfp/report/' + $stateParams.reportId,
                data: angular.toJson($scope.report)
            }).then(function successCallback(response) {
                console.log(response.data.data);
            });
        } else {
            $scope.report = create_new_report();
        }
    };

    $scope.intialize_report_options = function() {
        $('.date-picker').datepicker({
            autoclose: true,
            clearBtn: true,
            todayHighlight: true
        });
    }
    $scope.setStep = function(value) {
        console.log($scope.report);
        if (value == '2' && $scope.report.type == 'sale') {
            $scope.step = '3';
        } else if (value == '4') {
            $scope.step = '4';
        } else {
            $scope.step = value;
        }
    };

    $scope.email_metrics = [{
        'name': 'AS Emails Sent',
        'code': 'n_sent'
    }, {
        'name': 'AS Emails Opened',
        'code': 'n_opened'
    }, {
        'name': 'AS Emails Clicked',
        'code': 'n_clicked'
    }, {
        'name': 'AS Number of Clicks',
        'code': 'n_clicks'
    }, {
        'name': 'Market Research',
        'code': 'market_research'
    }, {
        'name': 'Offers',
        'code': 'offers'
    }];


    $scope.$on('$viewContentLoaded', function() {
        // initialize core components
        App.initAjax();
        var p_countries = load_countries();
        var p_metrics = load_metrics();
        $('.bs-select').selectpicker();
        var p_dims = load_dimensions();
        var p_communities = load_communities();
        var all = $q.all([p_countries, p_metrics, p_dims, p_dims, p_communities])
        all.then(function(){
            initialize_report();
        });
        console.log($scope.report);
    });
    $rootScope.settings.layout.pageContentWhite = true;
    $rootScope.settings.layout.pageBodySolid = false;
    $rootScope.settings.layout.pageSidebarClosed = false;
});