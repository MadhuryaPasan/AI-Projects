import { Button } from '@/components/ui/button'
import {
    Item,
    ItemActions,
    ItemContent,
    ItemDescription,
    ItemMedia,
    ItemTitle,
} from "@/components/ui/item"
import { File, Trash } from 'lucide-react'

const filecard = ({ name }: { name: string }) => {
    return (
        <Item variant="outline">
            <ItemMedia variant="icon">
                <File />
            </ItemMedia>
            <ItemContent>
                <ItemTitle>{name}</ItemTitle>
                {/* <ItemDescription>File Description</ItemDescription> */}
            </ItemContent>
            <ItemActions>
                <Button variant="destructive" size="icon">
                    <Trash />
                </Button>
            </ItemActions>
        </Item>
    )
}

export default filecard