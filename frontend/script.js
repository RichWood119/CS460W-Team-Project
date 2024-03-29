const firebaseConfig = {
    apiKey: "AIzaSyAclDJzi50FBG8anJ_F_fvxar6HCkEKvLs",
    authDomain: "cs460w-project.firebaseapp.com",
    databaseURL: "https://cs460w-project-default-rtdb.firebaseio.com",
    projectId: "cs460w-project",
    storageBucket: "cs460w-project.appspot.com",
    messagingSenderId: "266537356483",
    appId: "1:266537356483:web:53846e1fecfee208a1a676"
};

firebase.initializeApp(firebaseConfig);
const auth = firebase.auth();

document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const role = document.getElementById('role').value;

    auth.signInWithEmailAndPassword(username, password)
    .then((userCredential) => {
        const user = userCredential.user;
        console.log("User:", user.uid);

    })
    .catch((error) => {
        const errorCode = error.code;
        const errorMessage = error.message;
        console.error(errorMessage);
    });
});
