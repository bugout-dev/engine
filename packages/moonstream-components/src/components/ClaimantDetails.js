import React, { useContext } from "react";
import { Flex, Spinner, IconButton, Heading } from "@chakra-ui/react";
import Web3Context from "../core/providers/Web3Provider/context";
import { targetChain } from "../core/providers/Web3Provider";
import { CloseIcon } from "@chakra-ui/icons";
import { BiTrash } from "react-icons/bi";
import { useDrop } from "../core/hooks/dropper";
import useSearch from "../core/hooks/useSearch";
const ClaimantDetails = ({ claimId, address, onClose }) => {
  const web3ctx = useContext(Web3Context);

  const { deleteClaimants } = useDrop({
    targetChain,
    ctx: web3ctx,
    claimId: claimId,
  });

  const { search } = useSearch({
    pathname: "/drops/claimants/search",
    query: { address: address, dropper_claim_id: claimId },
  });
  if (search.isLoading) return <Spinner />;
  return (
    <Flex className="ClaimantDetails" direction={"row"} alignItems="baseline">
      {search.data?.address && (
        <>
          <Heading size="sm">Amount: {search.data.amount}</Heading>
          <IconButton
            size="sm"
            colorScheme="orange"
            isLoading={deleteClaimants.isLoading}
            onClick={() => {
              deleteClaimants.mutate(
                { list: [address] },
                {
                  onSuccess: () => {
                    search.remove();
                    onClose();
                  },
                }
              );
            }}
            version="ghost"
            icon={<BiTrash />}
          ></IconButton>
        </>
      )}
      {!search.data?.address && <Heading size="sm">Not found</Heading>}
      <IconButton
        colorScheme="orange"
        onClick={onClose}
        size="sm"
        version="ghost"
        icon={<CloseIcon />}
      ></IconButton>
    </Flex>
  );
};
export default ClaimantDetails;
