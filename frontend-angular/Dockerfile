FROM node:20-slim
WORKDIR /app
RUN apt-get -o APT::Sandbox::User=root update &&     apt-get -o APT::Sandbox::User=root install -y curl &&     npm install -g @angular/cli@latest
EXPOSE 4200
