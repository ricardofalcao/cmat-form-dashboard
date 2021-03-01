<template>
    <div class="preferences pa-4">
        <v-card elevation="2">
            <v-card-text>
                <h4 class="text-h4 mb-4">Preferences</h4>

                <v-form
                        ref="form"
                        v-model="valid">

                    <v-text-field
                            :disabled="pending"
                            v-model="form.newPassword"
                            type="password"
                            :rules="[
                                        v => !!v || 'Please insert your new password',
                                    ]"
                            label="New Password"
                            required
                    ></v-text-field>

                    <v-text-field
                            :disabled="pending"
                            v-model="form.newPasswordRepeat"
                            type="password"
                            :rules="[
                                        v => !!v || 'Please repeat your new password',
                                        v => v == form.newPassword || 'The passwords must match'
                                    ]"
                            label="Confirm Password"
                            required
                    ></v-text-field>

                    <v-btn
                            :disabled="pending"
                            class="mt-2"
                            type="submit"
                            color="success"
                            outlined

                            @click.prevent="changePassword"
                    >
                        Submit
                    </v-btn>

                    <v-snackbar
                            v-model="snackbar"
                    >
                        Password changed!

                        <template v-slot:action="{ attrs }">
                            <v-btn
                                    color="white"
                                    text
                                    v-bind="attrs"
                                    @click="snackbar = false"
                            >
                                Close
                            </v-btn>
                        </template>
                    </v-snackbar>

                    <span v-if="success"></span>
                </v-form>
            </v-card-text>
        </v-card>
    </div>
</template>

<script>
    export default {
        name: 'Preferences',
        data() {
            return {
                valid: false,
                pending: false,
                snackbar: false,
                form: {
                    newPassword: '',
                    newPasswordRepeat: ''
                }
            }
        },
        methods: {
            changePassword() {
                if (!this.valid) {
                    return;
                }

                this.pending = true;
                this.snackbar = false;

                fetch(`http://localhost:8000/api/users/me`, {
                    method: "PATCH",
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem("jwt")}`,
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({password: this.form.newPassword})
                })
                    .then(async response => {
                        const data = await response.json();

                        // check for error response
                        if (!response.ok) {
                            // get error message from body or default to response status
                            const error = (data && data.detail) || response.status;
                            return Promise.reject(error);
                        }

                        this.snackbar = true;

                        this.form.newPassword = '';
                        this.form.newPasswordRepeat = '';
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
