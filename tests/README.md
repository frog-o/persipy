# Testing

The setup for testing the project with with cloudflare python workers is in `/tests/wrangler`.

#### Usage

`RUN_SERVER.py` **starts** the wrangler worker as web server on your local ip (not just localhost) in secure context. It also when runs adds symlincs of the `/src` and `/dist` directories to the `assets` directory of the web server runing.

The `assets` directory is hosted at the very root so for example `/src/module.py` will be accessable at `https://192.168.0.2/src/module.py` (the ip adress if for the example). To make things easier whats in `/src` is also avaivable at the root so the same file will be at `https://192.168.0.2/module.py` as well.


#### Configuration and assets

`wrangler.toml` settings for running the server


`wrangler_worker/wrangler.py` the very server worker as simple possible


`assets/index.html` the index web page of the website with script tag
`<script type="mpy" src="index.py" config="config.toml" terminal></script>`
to start pyscript with the specified attributes.


`assets/index.py` the pyscript python file loaded in the script tag above by default, you can change it giving even some entry point from the source of your project.


`assets/config.toml` the pyscript settings


#### Requirements

To use all of that you will need the *cloudflare wrangler cli*.

You can install the **wrangler** using **npm**, which requires **Node.js**. If you don't have the latter, you can download and install it from [nodejs.org](nodejs.org). 

After you have Node.js (npm comes with it) you can install the **wrangler**:

```
npm install -g wrangler
```

You do not need an account in cloudflare to use it.

#### More info

[wrangler dec cli](https://developers.cloudflare.com/workers/wrangler/commands/#dev)

[wrangler install](https://developers.cloudflare.com/workers/wrangler/install-and-update/)

[Python in cloudflare workes](https://developers.cloudflare.com/workers/languages/python/)