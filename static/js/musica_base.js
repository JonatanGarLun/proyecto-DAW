// let isPlaying = false;
// let currentSongIndex = 0;
// let audio = null;
// let changeCooldown = false;
//
// const playPauseBtn = document.getElementById("playPauseBtn");
// const prevBtn = document.getElementById("prevBtn");
// const nextBtn = document.getElementById("nextBtn");
//
// function updateButtonStates() {
//     if (!songs.length) return;
//     prevBtn.disabled = currentSongIndex <= 0 || changeCooldown;
//     nextBtn.disabled = currentSongIndex >= songs.length - 1 || changeCooldown;
//     playPauseBtn.textContent = isPlaying ? '⏸️' : '▶️';
// }
//
// function toggleMusic() {
//     if (!audio) return;
//     if (isPlaying) {
//         audio.pause();
//     } else {
//         audio.play();
//     }
//     isPlaying = !isPlaying;
//     updateButtonStates();
// }
//
// function setCooldown(ms) {
//     changeCooldown = true;
//     updateButtonStates();
//     setTimeout(() => {
//         changeCooldown = false;
//         updateButtonStates();
//     }, ms);
// }
//
// function nextSong() {
//     if (changeCooldown || currentSongIndex >= songs.length - 1) return;
//     currentSongIndex++;
//     changeSong(currentSongIndex);
//     setCooldown(1500);
// }
//
// function prevSong() {
//     if (changeCooldown || currentSongIndex <= 0) return;
//     currentSongIndex--;
//     changeSong(currentSongIndex);
//     setCooldown(1500);
// }
//
// function changeSong(index) {
//     if (!songs[index]) return;
//     if (audio) audio.pause();
//     audio = new Audio(songs[index].url);
//     isPlaying = true;
//     audio.addEventListener('loadedmetadata', () => {
//         audio.currentTime = 0;
//         audio.play();
//         updateButtonStates();
//     });
//     audio.onended = () => nextSong();
// }
//
// window.addEventListener('load', () => {
//     if (songs.length === 1) {
//         prevBtn.style.display = 'none';
//         nextBtn.style.display = 'none';
//     }
//
//     if (songs.length === 0) {
//         prevBtn.style.display = 'none';
//         playPauseBtn.style.display = 'none';
//         nextBtn.style.display = 'none';
//     }
//
//     if (songs.length > 0) {
//         currentSongIndex = Math.floor(Math.random() * songs.length);
//         audio = new Audio(songs[currentSongIndex].url);
//         audio.onended = () => nextSong();
//         updateButtonStates();
//     }
// });