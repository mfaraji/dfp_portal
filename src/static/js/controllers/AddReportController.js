angular.module('InspireApp').controller('AddReportController', function($rootScope, $scope, $http, $state, $stateParams) {

    $scope.is_edit = false;
    $scope.$on('$viewContentLoaded', function() {
        // initialize core components
        App.initAjax();
        $scope.load_countries();
        $scope.load_metrics();
        $('.bs-select').selectpicker();
        $scope.load_dimensions();
        $scope.load_ad_units();
        $scope.load_communities();
        $scope.load_topics();
        // $scope.initialize_report_options();
    });

    $scope.report = {};
    $scope.step = "1";
    $scope.isDisabled = false;
    $scope.dimensions = [];
    $scope.all_dimensions = [];
    $scope.all_metrics = [];
    $scope.all_topics = [];
    $scope.communities = [];
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

    $scope.load_topics = function() {
        $http({
            method: 'GET',
            url: '/dfp/topics'
        }).then(function successCallback(response) {
            $scope.all_topics = response.data.result;
        });
    };

    $scope.load_communities = function() {
        $http({
            method: 'GET',
            url: '/dfp/communities'
        }).then(function successCallback(response) {
            $scope.communities = response.data.result;
        });
    };

    $scope.initialize_report_options = function() {
        console.log($scope.report.type);
        if ($scope.step == '2') {
            $scope.dimensions = _.filter($scope.all_dimensions, function(obj) {
                return _.includes(obj.type, $scope.report.type)
            });
        }
        if ($scope.step == '3' || $scope.step == '2') {
            $scope.metrics = _.filter($scope.all_metrics, function(obj) {
                return _.includes(obj.type, $scope.report.type)
            });
        }
        if ($scope.step == '4') {
            if ($scope.report.communities != undefined) {
                var coms = _.map($scope.report.communities, 'name');
                $scope.topics = _.filter($scope.all_topics, function(obj) {
                    return _.includes(obj.community, coms)
                });
            } else {
                $scope.topics = $scope.all_topics;
            }
        }
        $('.date-picker').datepicker({
            autoclose: true,
            clearBtn: true,
            todayHighlight: true
        });
    };

    $scope.setStep = function(value) {
        console.log($scope.report);
        if (value == '2' && $scope.report.type == 'sale') {
            $scope.step = '3';
        } else if (value == '4') {
            $scope.step = '4';
        } else {
            $scope.step = value;
        }
        console.log($scope.report);
    };

    $scope.format_topic_name = function(topic) {
        return topic.community + " > " + topic.name;
    };
    $scope.email_metrics = [{
        'name': 'Emails Sent',
        'code': 'n_sent'
    }, {
        'name': 'Emails Opened',
        'code': 'n_opened'
    }, {
        'name': 'Emails Clicked',
        'code': 'n_clicked'
    }, {
        'name': 'Number of Clicks',
        'code': 'n_clicks'
    },{
        'name': 'Summary',
        'code': 'summary'
    }, ];
    $rootScope.settings.layout.pageContentWhite = true;
    $rootScope.settings.layout.pageBodySolid = false;
    $rootScope.settings.layout.pageSidebarClosed = false;
});