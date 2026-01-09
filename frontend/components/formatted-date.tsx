import { cn } from "@/lib/utils"

interface FormattedDateProps extends React.HTMLAttributes<HTMLSpanElement> {
    date: string | Date | null | undefined
    options?: Intl.DateTimeFormatOptions
}

export function FormattedDate({
    date,
    options,
    className,
    ...props
}: FormattedDateProps) {
    if (!date) {
        return <span className={cn("text-muted-foreground italic", className)} {...props}>N/A</span>
    }

    const dateObj = new Date(date)

    // Check if date is valid
    if (isNaN(dateObj.getTime())) {
        return <span className={cn("text-destructive", className)} {...props}>Invalid Date</span>
    }

    const defaultOptions: Intl.DateTimeFormatOptions = {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        ...options
    }

    return (
        <span className={cn("whitespace-nowrap", className)} {...props}>
            {dateObj.toLocaleString(undefined, defaultOptions)}
        </span>
    )
}
