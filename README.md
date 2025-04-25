# The Flutterflow Starter Kit API

This is the repository of the [FlutterFlow Starter Kit](https://kealy.studio/flutterflow)'s Python API. The API serves many purposes in supporting a FlutterFlow project, such as

- Endpoints for sending push notifications and displaying notifications histories
- Creating and setting admin roles to users
- Sending email, including onboarding emails
- Interacting with Supabase, including token minting
- Interacting with Firebase, including Auth token decoding, custom claims setup, and Firestore interactions
- A configurable admin dashboard frontend, delivered statically as part of the API
- A framework for creating custom logic. Anything you can do in Python,
you can make available to your app.
- Pages for App store requirements such as support pages, terms of service, privacy policies, and data deletion requests.
- Media uploads with Cloudinary
- A full unit testing suite
- CI/CD workflows for deployments and database backups

You can work on the API locally alongside a local Supabase instance, and deploy the API to GCP whenever you're ready.


## Initial setup

First, you'll want to name your API, by renaming this root directory
and altering some of the basic settings in `settings.py`.

It's recommended to then start version controlling the project
using git from the very beginning (`git init`), and learning some
basic git workflows to keep your code stable.


## Create a `.env.local` file

`.env.local` is the convention used here for the file that holds your environment variables.
Environment variables are picked up by the `setting.py` module, which can then be used throughout your app. Environment files usually include secrets, so always
keep the contents of `.env.local` secure.

Some of these environment variables are obligatory, others are optional. Use the `.env.local.template` file
as the starting point, and rename it to `.env.local`. This rename will
prevent the file being checked into version control, which is very important
for security, so make sure to rename it.


## Directory structure

Inside of the `app/` directory you'll find the API itself. The entry point is `main.py`,
and from this module the API will initialize itself and mount all the other components.

`settings.py` is essential to this process, this is where the settings are applied
that pertain to your app. Most of the settings here will be set from environment variables you define in `.env.local`, but it's
good to know where these environment variables are injected. You may also add your own settings in this file too.


### The `models/` directory

`models` is a folder generally associated with schemas, the most common of which are
database schemas. However, since Supabase handles this, the `models` folder here is more
likely to be used with in-memory schema, which are usually defined using pydantic models.

You can learn more about pydantic [here](https://docs.pydantic.dev/latest/).

One essential module in the `models` folder is `__init__.py`, because it's here that I've
added the code for initializing Firebase. This is invoked in `main.py`, and it's configured
to rely on the environment in which the code is being run to provide the Firebase credentials. You can
learn how set up the Firebase credentials [here](https://kealy.studio/starterkit-docs/#pythonAPI).


### The `routers` directory

Routers (also called Views) are the entry point for API requests. You can define HTTP REST endpoints
(or other types of endpoint) like GET, POST, PATCH and DELETE here and return responses. Try
not to shove all your business logic or database interactions into views, instead, use services.

I've set an `admin` and a `user` directory here – these are not essential – it's just one way
to separate out endpoints with different levels of privilege. You'll find auth guards like
```python
Depends(get_admin_user)
```
and
```python
Depends(get_current_user)
```
here, and these are for decoding the Firebase JWT token and authorizing the user. They're  important for security, so be sure you understand their purpose and how they work.


### The `services/` directory

Most of your business logic and error handing should happen in this folder, and this
is also where you'll call the model layer and database layers. This is where the "core"
magic of what your application does should be handled.


## Testing

The Pytest unittest suite is very useful for keeping your app stable. It
works based on a local version of Supabase, and is also very useful for local
development in general. Spin up a local Supabase environment using
[this guide](https://kealy.studio/blog/the-supabase-cli/) to get started,
and use the Pytest option in the vscode debugger to run the tests.

You'll need to set the environment variables in `.env.local`as something like:
```bash
SUPABASE_URL=http://127.0.0.1:54321
SUPABASE_ANON_KEY=ey-get-this-key-from-supabase-status
SUPABASE_SECRET_KEY=ey-get-this-key-from-supabase-status
SUPABASE_JWT_SECRET=your-super-secret-jwt-token-with-at-least-32-characters-long
```
where the values can be found by running the `supabase status` command (after setting up the local instance using the Supabase CLI).



## Deployment

Since the API is stateless, you can deploy it on any provider you like:
Fly.io, Google Cloud Run, Render, Heroku, Digital Ocean, Linode, AWS Lamda,
AWS EC2, Railway... you get the picture.

My preference is Google Cloud Run, because you already have a GCP project
(your Firebase project) that you have to maintain anyway.


### Deployment to Google Cloud Run

The API has a `Dockerfile` at the root of the project. This file packages the
app up so that it can be run anywhere and will work just the same. Docker
will snapshot an "image" of the API, and then Google will deploy a version
of that image, known as a "container".

Images need to live somewhere, and in a GCP project, that somewhere is the
Artifacts Registry. Luckily, we don't need to care too much about this
as Google will build and store the images for us, but it's important to know
that Google is storing these images because sometimes old images will need
to be deleted to prevent exceeding the free tier.


#### Initial API deploy

You'll need the project ID, which you can get from the Firebase console. Choose a
GCP region, whichever is likely closest to your users. Choose a service name, it can
be the same as the name of the root directory from this repository,
so you can identify the running API service. And choose a YAML
environment-variables file, remembering that you ideally have at least two, one
for development and one for production.

You'll likely do the below steps more than once, one for each environment (dev, prod, etc).
If you want, you can just run the below all at once, but it's recommended to run the commands
one-by-one to address any errors.

```bash
# Log in as the project owner
gcloud auth login

# Add your project id and choose a value for the other fields here
export PROJECT_ID=
export REGION=us-central1
export SERVICE_NAME=
export ENV_FILE=.env.[ENVIRONMENT].yaml

# Set the current project
gcloud config set project $PROJECT_ID
gcloud auth application-default set-quota-project $PROJECT_ID

# Get the project number
PROJECT_NUMBER=`gcloud projects describe $(gcloud config get-value project) --format="value(projectNumber)"`

# Run the first deploy with the env variables. Subsequent deploys can be done via Github Actions (if set up)
gcloud run deploy $SERVICE_NAME --source . --region=$REGION --platform=managed --allow-unauthenticated --service-account="$PROJECT_NUMBER-compute@developer.gserviceaccount.com" --env-vars-file $ENV_FILE
```


#### Automated API deployments

Github is a very well known platform for storing code under version control. It's recommended to use `git`
locally in this repository to version your code in general, and Github is a nice platform to compliment that workflow
and keep your code safe in the cloud. When you push the code to Github, it triggers "Github Actions"
defined in the `.github/workflows/gcp-deploy.yaml` file.

These Actions deploy the code to Google Cloud Run. To set them up, you'll need to add secrets. These can be set
in the Github dashboard under Settings > Secrets & Variables > Actions.

First, you need to set GCLOUD_SERVICE_KEY_DEV and GCLOUD_SERVICE_KEY_PROD, one for development and one for production.
Run these commands to get it. It's base64 encoded to make it more portable.
```bash
# Create a credentials keyfile for the service account that will be in charge of deployments
gcloud iam service-accounts keys create keyfile.json --iam-account=$PROJECT_NUMBER-compute@developer.gserviceaccount.com

# Copy the base64 string from this command and paste it into Github actions
cat keyfile.json | base64 -w 0
```

After doing the above, DELETE THE KEYFILE or at least keep it somewhere safe elsewhere. DO NOT ACCIDENTALLY ADD IT TO THE
REPOSITORY OR COMMIT IT TO GIT.
```bash
rm keyfile.json
```

Note that the PROJECT_NUMBER will determine the environment, so follow the steps in the last section to get the PROJECT_NUMBER
for development and assign that to GCLOUD_SERVICE_KEY_DEV, and likewise get the production PROJECT_NUMBER for GCLOUD_SERVICE_KEY_PROD.
Be sure to test all of this thoroughly after setting it up.

You also need to set GCLOUD_PROJECT_DEV and GCLOUD_PROJECT_PROD, this just is the project ID, again one for each environment.

To deploy to develoment, you just need to push to the develop branch (you can also specify a different branch in the actions file). To deploy to production, create a [Release](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases) in Github.
