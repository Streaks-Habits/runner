FROM node:alpine as build

# Copy runner sources
WORKDIR /runner
COPY package.json package.json
COPY tsconfig.json tsconfig.json
COPY src src
# Install npm dependencies and build
RUN npm i
RUN npm run build


FROM node:alpine as main

# Install daemons dependencies
RUN apk add --no-cache python3 py3-pip
# Copy sources and builded sources
WORKDIR /runner
COPY package.json package.json
COPY --from=build /runner/dist ./dist
COPY daemons daemons
# Install python deps
RUN pip3 install -r daemons/requirements.txt
# Install only production
RUN npm install --production

CMD sh -c "npm start"
