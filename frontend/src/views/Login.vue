<template>
    <div class="login">
        <v-container fill-height>
            <v-layout align-center justify-center>
                <v-card
                        elevation="3"
                        max-width="400px"
                        width="90%"
                        :loading="pending"
                >
                    <v-card-text>
                        <v-form
                                v-model="valid"
                        >
                            <div>
                                <h4 class="text-h4  font-weight-regular text-center mb-4">Log in</h4>
                            </div>

                            <v-text-field
                                    v-model="form.username"
                                    :rules="[
                                        v => !!v || 'E-mail is required',
                                        v => /.+@.+\..+/.test(v) || 'E-mail must be valid',
                                    ]"
                                    label="Email"
                                    required
                            ></v-text-field>
                            <v-text-field
                                    v-model="form.password"
                                    type="password"
                                    :rules="[
                                        v => !!v || 'Password is required',
                                    ]"
                                    label="Password"
                                    required
                            ></v-text-field>

                            <v-btn
                                    :disabled="pending"
                                    type="submit"
                                    color="success"
                                    block
                                    outlined

                                    @click.prevent="loginUser"
                            >
                                <v-icon
                                        left
                                >
                                    mdi-lock
                                </v-icon>
                                Log in!
                            </v-btn>
                        </v-form>
                    </v-card-text>
                </v-card>
            </v-layout>
        </v-container>
    </div>
</template>

<script>
    export default {
        name: 'Login',
        data() {
            return {
                valid: true,
                pending: false,
                form: {
                    username: '',
                    password: ''
                }
            }
        },
        methods: {
            loginUser() {
                if(!this.valid) {
                    return;
                }

                this.pending = true;

                let formBody = [];
                for (let property in this.form) {
                    let encodedKey = encodeURIComponent(property);
                    let encodedValue = encodeURIComponent(this.form[property]);

                    formBody.push(encodedKey + "=" + encodedValue);
                }

                const requestOptions = {
                    method: "POST",
                    headers: {'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'},
                    body: formBody.join('&')
                };

                fetch("http://localhost:8000/api/auth/jwt/login", requestOptions)
                    .then(async response => {
                        const data = await response.json();

                        // check for error response
                        if (!response.ok) {
                            switch (response.status) {
                                case 400: {
                                    this.formErrors = ['Invalid username or password.'];
                                    break;
                                }

                                case 422: {
                                    this.formErrors = ['Please fill all the form fields.'];
                                    break;
                                }
                            }

                            // get error message from body or default to response status
                            const error = (data && data.detail) || response.status;
                            return Promise.reject(error);
                        }

                        localStorage.setItem('jwt', data.access_token)

                        if (this.$route.params.nextUrl != null) {
                            this.$router.push(this.$route.params.nextUrl)
                        } else {
                            this.$router.push('/')
                        }
                    })
                    .catch(error => {
                        console.log(error);
                    })
                    .finally(() => {
                        this.pending = false
                    });
            }
        }
    }
</script>
