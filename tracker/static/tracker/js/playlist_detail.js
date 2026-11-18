let player = null;
let playerReady = false;

let currentVideoId = null;
let currentVideoButton = null;

let completionSent = false;
let completionRequestInProgress = false;

let progressInterval = null;
let embeddingError = false;

console.log("Playlist JavaScript file loaded");


// Initialize YouTube player
window.onYouTubeIframeAPIReady = function () {

    console.log("YouTube API is ready");

    player = new YT.Player('youtubePlayer', {

        width: '100%',
        height: '390',

        playerVars: {
            playsinline: 1,
            rel: 0
        },

        events: {

            onReady: function () {
                playerReady = true;
                console.log("YouTube player is ready!");
            },

            onStateChange: onPlayerStateChange,
            onError: onPlayerError

        }

    });

};


// Handle video button clicks
document.addEventListener('click', function (event) {

    const button = event.target.closest('.video-item');

    if (!button) return;

    if (!playerReady || !player) {
        console.error("Player is not ready");
        return;
    }

    stopLiveProgress();

    currentVideoId = button.dataset.videoId;
    currentVideoButton = button;

    completionSent = false;
    embeddingError = false;

    document.getElementById('videoErrorMessage').style.display = 'none';
    document.getElementById('youtubePlayer').style.display = 'block';

    const manualButton = document.getElementById(
        'markVideoCompletedManually'
    );

    manualButton.disabled = false;

    const isCompleted = button.classList.contains('completed-video');

    manualButton.textContent = isCompleted
        ? 'Mark as Unfinished'
        : 'Mark as Completed';

    manualButton.classList.toggle('unfinished-button', isCompleted);

    document.getElementById('currentVideoTitle').textContent =
        button.dataset.videoTitle;

    document.getElementById('videoProgressPercentage').textContent = '0%';
    document.getElementById('videoProgressBar').style.width = '0%';

    console.log("Loading video:", currentVideoId);

    player.loadVideoById(currentVideoId);

});


// Handle YouTube player states
function onPlayerStateChange(event) {

    console.log("Player state changed:", event.data);

    if (event.data === YT.PlayerState.PLAYING) {
        startLiveProgress();
    }

    if (
        event.data === YT.PlayerState.PAUSED ||
        event.data === YT.PlayerState.BUFFERING
    ) {
        stopLiveProgress();
    }

    // Automatically mark video completed when it ends
    if (
        event.data === YT.PlayerState.ENDED &&
        currentVideoId &&
        !completionSent
    ) {

        stopLiveProgress();

        completionSent = true;

        saveVideoProgress(true, false);

    }

}


// Start live progress tracking
function startLiveProgress() {

    stopLiveProgress();

    updateLiveProgress();

    progressInterval = setInterval(function () {
        updateLiveProgress();
    }, 5000);

}


// Stop live progress tracking
function stopLiveProgress() {

    if (progressInterval) {
        clearInterval(progressInterval);
        progressInterval = null;
    }

}


// Update current video playback progress
function updateLiveProgress() {

    if (!player || !playerReady || !currentVideoId || embeddingError) {
        return;
    }

    const currentTime = player.getCurrentTime();
    const duration = player.getDuration();

    if (!duration || duration <= 0) {
        return;
    }

    const percentage = Math.min(
        100,
        Math.round((currentTime / duration) * 100)
    );

    document.getElementById('videoProgressPercentage').textContent =
        percentage + '%';

    document.getElementById('videoProgressBar').style.width =
        percentage + '%';

    const page = document.getElementById('playlistPage');

    const csrfToken = document.querySelector(
        '#csrfForm [name="csrfmiddlewaretoken"]'
    ).value;

    const formData = new URLSearchParams();

    formData.append('video_id', currentVideoId);
    formData.append('current_time', currentTime);

    fetch(page.dataset.progressUrl, {

        method: 'POST',

        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/x-www-form-urlencoded'
        },

        body: formData.toString()

    })

    .then(response => {

        if (!response.ok) {
            throw new Error("Could not save live progress");
        }

        return response.json();

    })

    .then(data => {

        if (data.success) {
            console.log("Live progress saved:", percentage + "%");
        }

    })

    .catch(error => {
        console.error("Live progress error:", error);
    });

}


// Update completion status
// true = completed
// false = unfinished
function saveVideoProgress(isCompleted, isManual = false) {


    if (!currentVideoId || !currentVideoButton) {
        return;
    }

    if (completionRequestInProgress) {
        return;
    }

    completionRequestInProgress = true;

    const videoId = currentVideoId;
    const videoButton = currentVideoButton;

    const page = document.getElementById('playlistPage');

    const csrfToken = document.querySelector(
        '#csrfForm [name="csrfmiddlewaretoken"]'
    ).value;

    const manualButton = document.getElementById(
        'markVideoCompletedManually'
    );

    if (isManual) {
        manualButton.disabled = true;
    }

    const formData = new URLSearchParams();

    formData.append('video_id', videoId);
    formData.append('is_completed', String(isCompleted));

    fetch(page.dataset.completionUrl, {

        method: 'POST',

        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/x-www-form-urlencoded'
        },

        body: formData.toString()

    })

    .then(response => {

        if (!response.ok) {
            throw new Error("Progress could not be updated");
        }

        return response.json();

    })

    .then(data => {

        console.log("Server response:", data);

        if (!data.success) {
            throw new Error(data.message || "Update failed");
        }

        // Update playlist percentage
        document.getElementById('progressPercentage').textContent =
            data.progress_percentage + '%';

        document.getElementById('progressBar').style.width =
            data.progress_percentage + '%';

        // Update completed video count
        document.getElementById('completedCount').textContent =
            data.completed_count + ' / ' +
            data.total_videos + ' videos completed';

        // Update selected video status
        const completedMark = videoButton.querySelector('.completed');
        // Update current video progress
        if (currentVideoButton === videoButton) {

            if (data.is_completed) {
                document.getElementById('videoProgressPercentage').textContent = '100%';
                document.getElementById('videoProgressBar').style.width = '100%';
            } else {
                document.getElementById('videoProgressPercentage').textContent = '0%';
                document.getElementById('videoProgressBar').style.width = '0%';
            }

        }

        if (data.is_completed) {

            videoButton.classList.add('completed-video');

            if (!completedMark) {

                const mark = document.createElement('span');

                mark.className = 'completed';
                mark.textContent = '✓';

                videoButton.appendChild(mark);

            }

        } else {

            videoButton.classList.remove('completed-video');

            if (completedMark) {
                completedMark.remove();
            }

        }

        // Update manual button label
        if (isManual && currentVideoButton === videoButton) {

            if (data.is_completed) {
                manualButton.textContent = 'Mark as Unfinished';
                manualButton.classList.add('unfinished-button');
            } else {
                manualButton.textContent = 'Mark as Completed';
                manualButton.classList.remove('unfinished-button');
            }

            manualButton.disabled = false;
        }

        console.log(
            data.is_completed
                ? 'Video marked as completed'
                : 'Video marked as unfinished'
        );

    })

    .catch(error => {

        console.error("Completion error:", error);

        if (isManual && currentVideoButton === videoButton) {
            manualButton.disabled = false;
        }

        if (!isManual) {
            completionSent = false;
        }

    })

    .finally(() => {

        completionRequestInProgress = false;

    });

}


// Handle YouTube player errors
function onPlayerError(event) {

    stopLiveProgress();

    console.error("YouTube player error:", event.data);

    if (
        (event.data === 150 || event.data === 101) &&
        currentVideoId
    ) {

        embeddingError = true;

        document.getElementById('youtubePlayer').style.display = 'none';

        document.getElementById('videoErrorMessage').style.display = 'block';

        document.getElementById('openYouTubeLink').href =
            'https://www.youtube.com/watch?v=' + currentVideoId;

        const manualButton = document.getElementById(
            'markVideoCompletedManually'
        );

        manualButton.textContent =
            currentVideoButton.classList.contains('completed-video')
                ? 'Mark as Unfinished'
                : 'Mark as Completed';

        // Add this immediately below
        manualButton.classList.toggle(
            'unfinished-button',
            currentVideoButton.classList.contains('completed-video')
        );

    } else {

        alert("YouTube player error code: " + event.data);

    }

}


// Manual completion toggle
document.getElementById('markVideoCompletedManually')
    .addEventListener('click', function () {

        if (
            !embeddingError ||
            !currentVideoId ||
            !currentVideoButton ||
            completionRequestInProgress
        ) {
            return;
        }

        // Determine the next status
        const nextStatus =
            !currentVideoButton.classList.contains('completed-video');

        saveVideoProgress(nextStatus, true);

    });
