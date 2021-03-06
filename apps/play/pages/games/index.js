import React from "react";
import { getLayout } from "../../../../packages/moonstream-components/src/layouts/EngineLayout";
import { Flex, Center } from "@chakra-ui/react";
import FeatureCard from "moonstream-components/src/components/FeatureCard";
const Games = () => {
  return (
    <Flex className="Games">
      <Flex
        w="100%"
        minH="100vh"
        bgColor={"blue.1200"}
        direction={"column"}
        px="7%"
        mt="100px"
      >
        <Center>
          <Flex>
            <FeatureCard
              w="300px"
              imgH="140px"
              link="games/cryptoUnicorns"
              text="A digital pet collecting and farming game, built on blockchain"
              //   heading="Crypto Unicorns"
              imageUrl={
                "https://s3.amazonaws.com/static.simiotics.com/crypto-unicorns/cu_logo.png"
              }
              alt="Crypto Unicorns"
              textColor={"white.100"}
              level="h2"
              imgPading={24}
              h="450px"
            />
            <FeatureCard
              w="300px"
              isExternal={true}
              link="https://conquest-eth.play.moonstream.to/"
              imgH="140px"
              text="Conquest.eth - An unstoppable and open-ended game of strategy and diplomacy running on the Ethereum Virtual Machine."
              //   heading="Conquest.eth"
              imageUrl={
                "https://s3.amazonaws.com/static.simiotics.com/conquest-eth/conquest_eth.png"
              }
              alt="Crypto Unicorns"
              textColor={"white.100"}
              level="h2"
              imgPading={24}
              //   disabled={true}
              h="450px"
            />
            {/* <video src="https://www.champions.io/static/karkadon-desktop-ee6012464e76b83dc149bd896368048a.mp4"></video> */}
            <FeatureCard
              w="300px"
              imgH="140px"
              link="games/crypto unicorns"
              text="Ascension is a blockchain game built by Jam City, an award-winning game company led by former MySpace co-founder and CEO Chris DeWolfe"
              //   heading="Champions Ascension"
              imageUrl={
                "https://s3.amazonaws.com/static.simiotics.com/champions-ascension/champions.png"
              }
              alt="Champions Ascension"
              textColor={"white.100"}
              level="h2"
              disabled={true}
              imgPading={24}
              h="450px"
            />
          </Flex>
        </Center>
      </Flex>
    </Flex>
  );
};

Games.getLayout = getLayout;

export default Games;
