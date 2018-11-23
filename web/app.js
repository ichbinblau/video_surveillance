var app = angular.module('app', ['ngAnimate', 'ui.bootstrap']);

app.controller('MainCtrl', function($scope, $log, $uibModal) {

  $scope.open = function(size, videoSource) {
    $log.info("open", videoSource);
    var modalInstance = $uibModal.open({
      animation: $scope.animationsEnabled,
      templateUrl: 'myModal.html',
      controller: 'ModalInstanceCtrl',
      backdrop: true,
      size: size,
      resolve: {
        videoSource: function() {
          return videoSource;
        }
      }
    });

    modalInstance.result.then(function(result) {
      //
    }, function() {
      $log.info('Modal dismissed at: ' + new Date());
    });
  };
  
  $scope.videoClick = function($event, videoSource) {
    $log.info("videoClick", videoSource)
    $scope.open('lg', videoSource);
  };

});

app.controller('ModalInstanceCtrl', function($scope, $uibModalInstance, videoSource, $log) {
  $log.info("ModalInstanceCtrl", videoSource);
  
  $scope.id = Math.floor((Math.random() * 100) + 1);
  $scope.videoSource = videoSource;
  
  $scope.ok = function() {
    $uibModalInstance.close('ok');
  };

  $scope.cancel = function() {
    $uibModalInstance.dismiss('cancel');
  };
});

app.controller(
  'videocontroller',
  function($scope) {

    $scope.pageNum = 0;
    $scope.pageSize = 3;
    $scope.isFirstPage = function() {
      return $scope.pageNum === 0;
    };
    $scope.isLastPage = function() {
      return $scope.pageNum >= Math.floor($scope.videoSources.length / $scope.pageSize);
    };
    $scope.prevPage = function() {
      $scope.pageNum--;
    };
    $scope.nextPage = function() {
      $scope.pageNum++;
    };
    $scope.videoSources = [
      'http://10.239.76.185/video/x264-output.mp4',
      'http://www.sample-videos.com/video/mp4/720/big_buck_bunny_720p_1mb.mp4',
      'http://www.quirksmode.org/html5/videos/big_buck_bunny.mp4',
      'http://www.sample-videos.com/video/mp4/720/big_buck_bunny_720p_1mb.mp4',
      'http://Video/Digital_Hiring.mp4',
      'http://www.sample-videos.com/video/mp4/720/big_buck_bunny_720p_1mb.mp4'
    ];

});

app.controller('ctrl', function($scope){
    $scope.$watch('$viewContentLoaded', function(){
            //do something
            //alert('1');
    });
    $scope.headers = ['datetime', 'camera id', 'detected objects', 'details'];
    $scope.alarms = [
        {'datetime': '2018-11-19 17:18', 'cameraid': '1', 'detected_objects': 'person', 'source': 'http://10.239.76.185/video/x264-output.mp4'},
        {'datetime': '2018-11-19 17:18', 'cameraid': '1', 'detected_objects': 'cell phone', 'source': 'http://Video/Digital_Hiring.mp4'},
        {'datetime': '2018-11-19 17:18', 'cameraid': '1', 'detected_objects': 'monitor', 'source': 'http://Video/Digital_Hiring.mp4'},
        {'datetime': '2018-11-19 17:18', 'cameraid': '1', 'detected_objects': 'person', 'source': 'http://Video/Digital_Hiring.mp4'},
        {'datetime': '2018-11-19 17:18', 'cameraid': '1', 'detected_objects': 'person', 'source': 'http://Video/Digital_Hiring.mp4'},
    ];
});


app.filter("trustUrl", ['$sce', function($sce) {
  return function(recordingUrl) {
    return $sce.trustAsResourceUrl(recordingUrl);
  };
}]);

app.filter(
  'paginate',
  function() {
    console.log('creating paginate function', arguments);
    return function(inputArray, pageNumber, pageSize) {
      console.log('paginating', arguments);
      pageNumber = pageNumber || 0;
      pageSize = pageSize || 4;
      if (!Array.isArray(inputArray))
        return inputArray;
      return inputArray.slice(pageNumber * pageSize, (pageNumber + 1) * pageSize);
    };
  });
