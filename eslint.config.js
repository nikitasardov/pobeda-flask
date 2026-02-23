import globals from "globals";

export default [
    {
        files: ["static/js/**/*.js"],
        languageOptions: {
            ecmaVersion: 2022,
            sourceType: "script",
            globals: {
                ...globals.browser,
                bootstrap: "readonly",
            }
        },
        rules: {
            "no-unused-vars": "warn",
            "no-undef": "error",
            "eqeqeq": "warn",
        }
    }
];
